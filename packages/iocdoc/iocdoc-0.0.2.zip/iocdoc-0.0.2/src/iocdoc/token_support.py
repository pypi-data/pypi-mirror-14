'''
Applies Python :mod:`tokenize` analysis to each line of a text file.
'''


import token
import tokenize
from utils import logMessage, strip_quotes
import text_file


PRINT_DIAGNOSTICS = False


class TokenLog():
    '''
    Applies the Python <code>tokenize</code> analysis
    to each line of a file.  This allows a lexical analysis
    of the file, line-by-line.  This is powerful and makes
    some complex analyses more simple but it assumes the file
    resembles Python source code.

    :note The <code>tokenize</code> analysis is not robust.  
          Some files will cause exceptions for various reasons.

    :see http://docs.python.org/library/tokenize.html
    :see http://docs.python.org/library/token.html
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.tokenList = []
        self.xref = {}
        self.nameTable = token.tok_name
        self.nameTable[tokenize.COMMENT] = 'COMMENT'
        self.nameTable[tokenize.NL] = 'NEWLINE'
        self.token_pointer = None
        if PRINT_DIAGNOSTICS:
            print "\n".join( sorted(self.nameTable.values()) )

    def get(self, index):
        '''
        retrieve the indexed token from the list
        '''
        return self.tokenList[index]

    def tokenName(self, tokType):
        '''
        convert token number to a useful string
        '''
        return self.nameTable[tokType]

    def tokenReceiver(self, tokType, tokStr, start, end, tokLine):
        '''
        called by tokenize package, logs tokens as they are called
        '''
        tokName = self.tokenName(tokType)
        tok_dict = {
            'tokName': tokName,
            'tokType': tokType,
            'tokStr': tokStr,
            'start': start,
            'end': end,
            'tokLine': tokLine,
        }
        self.tokenList.append( tok_dict )
        if not tokName in self.xref:
            self.xref[tokName] = []
        self.xref[tokName].append( len(self.tokenList)-1 )

    def getTokenList(self):
        '''
        :return: list of token dictionaries
        '''
        return self.tokenList

    def getCrossReferences(self):
        '''
        :return: dictionary of token cross-references
        '''
        return self.xref

    def report(self):
        '''
        prints (to stdout) results contained in tokenList list and xref dictionary
        '''
        print len(self.tokenList), "tokens were found"
        print len(self.xref), "different kinds of tokens were found"
        for k, v in self.xref.items():
            print k, len(v), "[",
            for index in v:
                report_dict = self.tokenList[index]
                print report_dict['start'][0],
            print "]"
        for k in ['OP', 'NAME', 'STRING']:
            if k in self.xref:
                for index in self.xref[k]:
                    report_dict = self.tokenList[index]
                    print k, report_dict['start'], "|" + report_dict['tokStr'].strip() + "|"

    def summary(self, alsoPrint = False):
        '''
        Summarizes the xref dictionary contents.
        Reports number of each different token name (type).

        :param alsoPrint: boolean to enable print to stdout
        :return: dictionary of token frequencies
        '''
        summary_dict = {k: len(v) for k, v in self.xref.items()}
        if alsoPrint:
            for k, v in sorted(summary_dict.items()):
                print "%s : %d" % (k, v)
        return summary_dict

    def processFile(self, filename):
        '''
        process just one file
        '''
        f = text_file.read(filename)    # use the file cache
        try:
            tokenize.tokenize(f.iterator().readline, self.tokenReceiver)
        except Exception, _exc:
            f.close()   # remember to close the file!
            msg = 'trouble with: ' + filename
            msg += '\n' + str(_exc)
            logMessage(msg)
            raise RuntimeError(msg)
        self.token_pointer = None
        f.close()

    def lineAnalysis(self):
        '''
        analyze the tokens by line

        :return dictionary with all the lines, including tokenized form
        '''
        # build a dictionary with all the lines, and a list of all the lines, in order
        lines = {'numbers':[]}
        longest = len(self.tokenList)
        lastProgress = None
        for tok in self.tokenList:
            lineNum = tok['start'][0]
            progress = lineNum*100/longest
            if progress != lastProgress:
                lastProgress = progress
                #if (progress % 5) == 0:
                #    print "%3d%%" % progress
            if not lineNum in lines['numbers']:
                # remember the order the line numbers came in
                lines['numbers'].append( lineNum )
                # each line number has a dictionary with:
                #   - (string) full text of the line from f.readline()
                #   - (string) token pattern
                #   - (list) tuple:  tokName, tokType, tokStr, start, end
                lines[lineNum] = {}
                lines[lineNum]['pattern'] = []
                lines[lineNum]['tokens'] = []
                lines[lineNum]['readline'] = tok['tokLine']
            # initially, pattern is a list of token names
            lines[lineNum]['pattern'].append( tok['tokName'] )
            item = { 'tokName': tok['tokName'], 
                     'tokType': tok['tokType'],
                     'tokStr': tok['tokStr'],
                     'start': tok['start'], 
                     'end': tok['end'] }
            lines[lineNum]['tokens'].append( item )
        # change pattern from list to string
        for line in lines['numbers']:
            pat = lines[line]['pattern']
            lines[line]['pattern'] = " ".join( pat )
        # don't retain this list locally, just return it to the caller
        return lines

    def setTokenPointer(self, position = None):
        '''
        set the token pointer to the given position
        
        :param position: index position within list of tokens
        :raise Exception: token pointer position errors
        '''
        if position != None:
            if position < 0:
                # allow easy Pythonic reference to the last indices
                position = len(self.tokenList) + position
            if position < 0:
                raise Exception, "position cannot be a negative number"
            if position >= len(self.tokenList):
                raise Exception, "position cannot be greater than or equal to number of tokens"
        self.token_pointer = position
        return self.tokenList[position]
    
    def getCurrentToken(self):
        return self.tokenList[self.token_pointer]

    #def __iter__(self):
    #    '''
    #    this class satisfies Python's iterator interface
    #    http://docs.python.org/reference/datamodel.html
    #    http://docs.python.org/library/stdtypes.html#typeiter
    #    '''
        
    def next(self):
        '''
        return the next token or raise a StopIteration exception 
        upon reaching the end of the sequence

        :return: token object
        :raise StopIteration: reached the end of the sequence
        '''
        if self.token_pointer == len(self.tokenList) - 1:
            raise StopIteration
        if self.token_pointer == None:
            self.token_pointer = -1
        self.token_pointer += 1
        return self.tokenList[self.token_pointer]
        
    def previous(self):
        '''
        return the previous token

        :return: token object
        :raise StopIteration: reached the beginning of the sequence
        '''
        if self.token_pointer == 0:
            raise StopIteration
        if self.token_pointer == None:
            self.token_pointer = 0
        self.token_pointer -= 1
        return self.tokenList[self.token_pointer]
        
    def nextActionable(self, skip_list=None):
        '''
        walk through the tokens and find the next actionable token
        
        :param (str) skip_list: list of tokens to ignore 
           
           default list: ('COMMENT', 'NEWLINE', 'ENDMARKER', 
            'ERRORTOKEN', 'INDENT', 'DEDENT')

        :return: token object or None if no more tokens
        '''
        # TODO: can this become an iterator?
        if skip_list is None:
            skip_these_tokens = ('COMMENT', 'NEWLINE', 'ENDMARKER', 
                                 'ERRORTOKEN', 'INDENT', 'DEDENT')
        else:
            skip_these_tokens = skip_list
        found = False
        while not found:
            try:
                token = self.next()
            except StopIteration:
                return None
            if token['tokName'] not in skip_these_tokens:
                found = True
        return token

    def _print_token_(self, tkn):
        '''developer use'''
        print '%3d,%3d' % tkn['start'], 
        print '%10s' % tkn['tokName'], 
        print '|%15s|' % tkn['tokStr'].strip(), 
        print '|%s|' % tkn['tokLine'].strip()
    
    def tokens_to_list(self):
        '''
        parse an enclosed list of tokens into a list
        
        Assume ``token_pointer`` is pointing at start terminator
        
        examples::
        
            (DESC, "motor $(P)$(M)") --> ['DESC', 'motor $(P)$(M)']
            {P,      S, BL,    T1, T2, A}  --> ['P', 'S', 'BL', 'T1', 'T2', 'A']
            {12ida1: A  "##ID" 1   2   1}  --> ['12ida1:', 'A', '##ID', '1', '2', '1']
            
            TODO: alias($(IOC):IOC_CPU_LOAD,"$(IOC):load")
    
        '''
        # first, decide the list terminators
        tok = self.getCurrentToken()
        t_start = token_key(tok)
        if t_start not in ('OP (', 'OP {'):
            msg = 'incorrect token type'
            raise ValueError, msg
        t_end = {'OP (': 'OP )', 'OP {': 'OP }'}[t_start]
        #content_names = ('NAME', 'NUMBER', 'OP', 'STRING', 'ERRORTOKEN')
        skip_list = ('COMMENT', 'NEWLINE', 'ENDMARKER', 
                #'ERRORTOKEN', 
                'INDENT', 'DEDENT')
        v = ''
        end = tok['start'][1]
        items = []
        depth = 1
        while depth>0 or token_key(tok) not in ('', t_end):
            tok = self.nextActionable(skip_list)
            key = token_key(tok)
            if key == t_start:
                depth += 1
            elif key == t_end:
                depth -= 1
                if depth == 0:
                    break
            if tok['start'][1] == end and key != 'OP ,':
                v += tok['tokStr']
                end = tok['end'][1]
            else:
                if len(v) > 0:
                    v = strip_quotes(v)
                    if len(v) == 0:  v = '""'
                    items.append(v)
                if key not in (t_end, 'OP ,'):
                    v = tok['tokStr']
                else:
                    v=''
                end = tok['end'][1]
    
        if len(v) > 0:      # last chance
            v = strip_quotes(v)
            if len(v) == 0:  v = '""'
            items.append(v)
    
        return items
    
    def getFullWord(self):
        '''
        parse the token stream for a contiguous word and return it as str
        
        Some words in template files might not be enclosed in quotes
        and thus the whole word is broken into several tokens.
        This command rebuilds the word, without stripping quotes (if provided).
        '''
        tok = self.getCurrentToken()
        end = tok['start'][1]
        v = ''
        while tok is not None:
            if tok['start'][1] == end:
                v += tok['tokStr']
                end = tok['end'][1]
            else:
                break
            tok = self.nextActionable()
        if v.endswith('{'):     # moved from template.py
            # watch for patterns such as this: "../../33iddApp/Db/filterDrive.db"{
            v = v[:-1]
            tok = self.setTokenPointer(self.token_pointer-1)    # undo last nextActionable()
            while token_key(tok) != 'OP {':
                tok = self.setTokenPointer(self.token_pointer-1)    # back up
        return v
    
    def getKeyValueSet(self):
        '''
        parse a token sequence as a list of macro definitions into a dictionary
        
        example::
        
            { P=12ida1:,SCANREC=12ida1:scan1 }
            {P=12ida1:,SCANREC=12ida1:scan1,Q=m1,POS="$(Q).VAL",RDBK="$(Q).RBV"}

        '''
        # TODO: what about reset definitions?  {P=,SCANREC=}
        kv = {}
        for definition in self.tokens_to_list():
            k, v = [_.strip('"') for _ in definition.split('=')]
            kv[k.strip()] = v
        return kv



def token_key(tkn):
    '''developer use, short string identifying the type and text of this token'''
    if tkn is None:
        m = ''
    else:
        m = tkn['tokName'] + ' ' + tkn['tokStr']
    return m


def parse_bracketed_macro_definitions(tokenLog):
    '''
    walk through a bracketed string, keeping track of delimiters
    
    verify we start on an opening delimiter
    '''
    analysis = _find_sections(tokenLog)

    token_dividers = [analysis['start'], analysis['end']]
    for key in 'commas equals'.split():
        token_dividers += analysis[key]
    token_dividers.sort()
    
    if len(analysis['commas']) == 0 and len(analysis['equals']) == 0:
        # No delimiters found: either no macro, 1 macro, or space-delimited.
        # Cannot become a dict since no "=" were found.
        # Look at all tokens between the enclosure, 
        # accumulate contiguous text,
        # break on non-contiguous boundaries
        # Note: makes no assumption about all on one line.
        s, f = token_dividers
        l, c = tokenLog.get(s)['end']
        text = ''
        parts = []
        for i in range(s+1, f):
            tok = tokenLog.get(i)
            if tok['start'][1] != c or tok['start'][0] != l:
                if len(text) > 0:
                    parts.append(text)
                text = tok['tokStr']
            else:
                text += tok['tokStr']
            l, c = tokenLog.get(i)['end']
        if len(text) > 0:
            parts.append(text)
        return parts

    text_list = []
    for index, key in enumerate(token_dividers[0:-1]):
        s = key+1
        f = token_dividers[index+1]
        text_list.append( _rebuild_text([tokenLog.get(_) for _ in range(s, f)]) )
    
    if len(analysis['commas']) > len(analysis['equals']):
        return text_list
    else:
        # tricky: http://stackoverflow.com/questions/6900955/python-convert-list-to-dictionary
        # if text_list = ['a', 'b', 'c', 'd']
        # this returns dict(a='b', c='d')
        return dict(zip(text_list[::2], text_list[1::2]))


def _find_sections(tokenLog):
    '''
    locate the tokens that divide this sequence into sections
    
    The overall section is delimited by {} or ().
    Internally, the delimiters are , or =.
    All the rest (that is not a comment) is string content to be kept.
    Return the sections as a a dictionary with these members:
    
    * 'open': token number for the opening symbol
    * 'commas': list of token numbers for comma delimiters
    * 'equals': list of token numbers for equal sign delimiters
    * 'close': token number for the matching closing symbol
    '''
    terminator = {
                  '{': 'OP }',
                  '(': 'OP )',
                  }
    
    tok = tokenLog.getCurrentToken()
    c = tok['tokStr']
    if c not in terminator:
        l, c = tok['start']
        msg = '(%d,%d) ' % (l, c+1)
        msg += 'token stream not starting with "(" or "{"'
        raise KeyError, msg

    pt_start = tokenLog.token_pointer
    tk_start = token_key(tok)
    tk_end = terminator[c]
    depth = 1
    tok = tokenLog.nextActionable()
    commas = []
    equals = []
    while depth > 0:
        tk = token_key(tok)
        if tk == 'OP ,' and depth == 1:
            commas.append(tokenLog.token_pointer)
        elif tk == 'OP =' and depth == 1:
            equals.append(tokenLog.token_pointer)
        elif tk == tk_start:
            depth += 1
        elif tk == tk_end:
            depth -= 1
            if depth == 0:
                pt_end = tokenLog.token_pointer
        tok = tokenLog.nextActionable()
    
    return dict(
                start = pt_start,
                end = pt_end,
                commas = commas,
                equals = equals,
                )


def _rebuild_text(token_list):
    '''
    reconstruct the text from the list of tokens
    '''
    text = ''
    for tok in token_list:
        # Q: What if tok['tokName'] is a COMMENT or other undesirable?
        # A: not common in macro definitions, fix code if this is seen
        # Q: what about line number or column number gaps between tokens?
        # A: addressed above, do not mix comma delimited and whitespace delimited
        text += tok['tokStr']
    return text


def reconstruct_line(tokens = [], firstIndex = 1):
    '''
    reconstruct the line from the list of tokens presented
    
    :param tokens: as used throughout this module
    :param firstIndex: first index in tokens list to use
    :return: reconstructed line
    '''
    cmd = ""
    for tkn in tokens[firstIndex:]:
        if tkn['tokName'] not in ('NEWLINE'):
            start = tkn['start'][1]
            cmd += " "*(start - len(cmd))
            cmd += tkn['tokStr']
    return cmd


######################################################################


def main():
    filename = __file__
    obj = TokenLog()
    obj.processFile(filename)
    obj.summary(True)
    analysis = obj.lineAnalysis()
    for number in analysis['numbers']:
        pattern = analysis[number]['pattern']
        print number
        if pattern not in ('NEWLINE', 'ENDMARK', 'COMMENT NEWLINE', ):
            print number, pattern, analysis[number]['readline'].strip()
    for _i in range(5):
        print str(obj.nextActionable())
    obj.setTokenPointer(-10)
    tok = obj.nextActionable()
    while tok != None:
        print str(tok)
        tok = obj.nextActionable()


if __name__ == '__main__':
    main()
