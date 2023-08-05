'''
EPICS template (substitutions) file analysis
'''

import os

import command_file
import database
import macros
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions
from utils import logMessage, FileRef


class DatabaseTemplateException(Exception): pass


class Template(object):
    '''
    EPICS template (substitutions) file
    
    Template files contain one or more database groups, 
    each containing one or more EPICS PV declarations.
    It is implied that each PV declaration is a call to 
    ``dbLoadRecords`` where the database is specified 
    in the database group header.
    '''
    
    def __init__(self, filename, ref, **env):
        self.filename = filename
        self.macros = macros.Macros(**env)
        self.filename_expanded = self.macros.replace(filename)

        self.database_list = []
        self.reference = ref
        self.commands = []

        self.source = text_file.read(self.filename_expanded)
        self.parse()
    
    def __str__(self):
        return 'dbLoadTemplate ' + self.filename + '  ' + str(self.macros)
    
    def _make_ref(self, tok, item=None):
        '''make a FileRef() instance for this item'''
        return FileRef(self.filename, tok['start'][0], tok['start'][1], item or self)
    
    def parse(self):
        '''
        interpret the template file for database declarations
        
        The Python tokenizer makes simple work of parsing database files.
        The TokenLog class interprets the contents according to a few simple terms
        such as NAME, OP, COMMENT, NEWLINE.
        '''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename_expanded)
        tok = tokenLog.nextActionable()
        actions = {
                   'NAME file': self._parse_file_statement,
                   'NAME global': self._parse_globals_statement,
                   }
        while tok is not None:
            tk = token_key(tok)
            if tk in actions:
                actions[tk](tokenLog)
            tok = tokenLog.nextActionable()

    
    def _parse_file_statement(self, tokenLog):
        '''
        support the *file* statement in a template file
        
        example::
        
            file "$(SSCAN)/sscanApp/Db/scanParms.db"
        
        '''
        ref = self._make_ref(tokenLog.getCurrentToken(), 'database file')
        # TODO: Do something with ref
        
        tok = tokenLog.nextActionable()
        dbFileName = tokenLog.getFullWord().strip('"')
        fname = self.macros.replace(dbFileName)

        tok = tokenLog.nextActionable()

        # When there is a "pattern" statement, 
        # the macro labels are given first, 
        # then (later) values in each declaration (usually multiple sets)
        pattern_keys = []
        if token_key(tok) == 'NAME pattern':
            tok = tokenLog.nextActionable()
            pattern_keys = tokenLog.tokens_to_list()
            tok = tokenLog.nextActionable()     # skip past the closing }
        
        while token_key(tok) != 'OP }':
            # define the macros for this set
            pattern_macros = macros.Macros(**self.macros.db)
            if len(pattern_keys) > 0:
                # The macro labels were defined in a pattern statement
                value_list = tokenLog.tokens_to_list()
                kv = dict(zip(pattern_keys, value_list))
                pattern_macros.setMany(**kv)
                tok = tokenLog.nextActionable()
            else:
                # No pattern statement, macro labels are defined with the values
                tok = tokenLog.getCurrentToken()
                kv = tokenLog.getKeyValueSet()
                pattern_macros.setMany(**kv)
                tok = tokenLog.nextActionable()
            
            ref = self._make_ref(tokenLog.getCurrentToken())
            # TODO: work out how to get the path into the next statement
            cmd = command_file.Command(self, '(dbLoadRecords)', 'path unknown', fname, ref, **pattern_macros.db)
            self.commands.append(cmd)
            dbg = database.Database(self, fname, ref, **pattern_macros.db)
            self.database_list.append(dbg)
    
    def _parse_globals_statement(self, tokenLog):
        '''
        support the *globals* statement in a template file
        
        This statement was new starting with EPICS base 3.15
        
        example::
        
            global { P=12ida1:,SCANREC=12ida1:scan1 }
        
        '''
        ref = self._make_ref(tokenLog.getCurrentToken(), 'global macros')
        # TODO: How to remember where the globals were defined?
        tok = tokenLog.nextActionable()
        if token_key(tok) == 'OP {':
            kv = parse_bracketed_macro_definitions(tokenLog)
            ref = self._make_ref(tok, kv)
            # TODO: Do something with ref
            self.macros.setMany(**kv)
        else:
            msg = '(%s,%d,%d) ' % (self.filename, tok['start'][0], tok['start'][1])
            msg += 'missing "{" in globals statement'
            raise DatabaseTemplateException(msg)
    
    def getPVList(self):
        pv_list = []
        for db in self.database_list:
            pv_list += db.getPVList()
    
    def getPVs(self):
        pv_dict = {}
        for db in self.database_list:
            for k, v in db.getPVs():
                pv_dict[k] = v
        return pv_dict.items()
    
    def get_databases(self):
        return self.database_list


def main():
    testfiles = []
    db = {}
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'example.template'))
    testfiles.append(os.path.join('.', 'testfiles', 'templates', 'omsMotors'))
    env = dict(TEST="./testfiles")
    for i, tf in enumerate(testfiles):
        try:
            ref = FileRef(__file__, i+1, 0, 'testing')
            db[tf] = Template(tf, ref, **env)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
    for k in testfiles:
        if k in db:
            print db[k].source.number_of_lines, k
            for command in db[k].commands:
                print str(command)
            for pvname, pv in sorted(db[k].getPVs()):
                ref = pv.reference
                print '\t(%s,%d,%d)\t%015s : %s' % (ref.filename, ref.line_number, ref.column_number, pv.RTYP, pvname)
    pass


if __name__ == '__main__':
    main()
