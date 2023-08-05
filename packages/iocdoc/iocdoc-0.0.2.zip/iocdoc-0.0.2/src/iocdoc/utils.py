'''
common routines for many modules

============================= ====================================================
support                       description
============================= ====================================================
:func:`chdir`                 change current IOC shell directory
:func:`datenow`               get a file either from the cache or from storage
:func:`detailedExceptionLog`  log the details of an exception
:class:`FileRef`              associate filename and line number of an object
:func:`logMessage`            log a message
:func:`strip_outer_pair`      remove outer symbols from text
:func:`strip_outer_quotes`    strip outer quotes (either single or double) from text
:func:`remove_comments`       strip out a C-style comment 
:const:`LOG_FILE`             default log file name 
:func:`strip_parentheses`     remove outer parentheses from text
:func:`strip_quotes`          strip outer double quotes from text
============================= ====================================================
'''


import datetime
import logging
import os
import re
import sys


C_LANGUAGE_COMMENT_RE = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
C_LANGUAGE_COMMENT_PATTERN = re.compile(
        C_LANGUAGE_COMMENT_RE,
        re.DOTALL | re.MULTILINE
    )

LOG_FILE = 'iocdoc.log'
logging_started = False


def chdir(newDir, nfsMounts={}):
    '''
    change the current working directory for the IOC shell

    :param newDir: name of new directory
    :return: success (True) or failure (False) 
    '''
    newDir = strip_quotes(newDir)
    if not os.path.exists(newDir):
        logMessage("cannot chdir(%s)" % newDir)
        # FIXME: fails with chdir(''), , needs to know the default to be used
        # FIXME: fails with chdir('/xorApps/...'), need to check the nfsMount dictionary
        return False
    pwd = os.getcwd()
    if pwd != newDir:
        logMessage("leave: "+ pwd)
        logMessage("enter: "+ newDir)
    os.chdir(newDir)
    return True


def datenow():
    '''return date and time now as a string'''
    return str(datetime.datetime.now())


def detailedExceptionLog(title='', print_traceback=True):
    '''
    enter details of an exception to the log (developer tool)
    '''
    import traceback
    if len(title) > 0:
        logMessage(title)
    info = sys.exc_info()
    logMessage(str(info[0]))
    logMessage(info[1])
    if print_traceback:
        #traceback.print_exc()
        logMessage(traceback.format_exc())


class FileRef(object):
    '''associate filename and line number of an object'''
    
    def __init__(self, filename, linenumber, colnumber, obj):
        self.filename = filename
        self.line_number = linenumber
        self.column_number = colnumber
        self.object = obj
    
    def __str__(self):
        # return '(%s,%d,%d) %s' % (self.filename, self.line_number, self.column_number, str(self.object))
        # TODO: can this be brief yet unambiguous?
        fname = os.path.split(self.filename)[-1]
        return '(%s,%d,%d)' % (fname, self.line_number, self.column_number)


def logMessage(text):
    '''
    log a message
    '''
    global logging_started
    if not logging_started:
        logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.INFO)
        #logging.basicConfig(level=logging.INFO)
        logging_started = True
    logging.info(' ' + datenow() + ' ' + str(text))
    print text
    sys.stdout.flush()

def remove_comments(text):
    '''
    strip out a C-style comment
    
    ::
    
       /* such as this */
    
    :see: http://stackoverflow.com/questions/241327/python-snippet-to-remove-c-and-c-comments
    '''
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s
    return re.sub(C_LANGUAGE_COMMENT_PATTERN, replacer, text)


def strip_outer_pair(text, left, right = None):
    '''
    remove outer symbols from text

    :param text: string
    :param left: symbol on left side
    :param right: symbol on right side (default is left-side symbol)
    :return: modified string
    :raise Exception: left and right must have len(..) == 1
    '''
    if right == None:
        right = left
    if len(left) != 1:
        raise Exception, "left symbol must be a single character, given: %s"%left
    if len(right) != 1:
        raise Exception, "right symbol must be a single character, given: %s"%right
    txt = text.strip()
    # only strip if both are present
    if txt[0] == left and txt[-1] == right:
        txt = txt[1:-1]
    return txt


def strip_outer_quotes(text):
    '''
    strip outer quotes (either single or double) from text

    :return: text without comments
    '''
    s0 = text[0]
    result = text
    if s0 in ('"', "'"):
        result = strip_outer_pair(text, s0)
    return result


def strip_parentheses(text):
    '''
    remove outer parentheses from text

    :param text: string
    :return: modified string
    '''
    return strip_outer_pair(text, "(", ")")


def strip_quotes(text, quote='"'):
    '''
    strip outer double quotes from text

    :return: text without comments
    '''
    if len(text) > 0 and text[-1] == quote:
        text = text[:-1]
    if len(text) > 0 and text[0] == quote:
        text = text[1:]
    return text
