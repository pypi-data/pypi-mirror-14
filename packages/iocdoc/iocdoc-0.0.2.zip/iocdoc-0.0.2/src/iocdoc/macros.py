'''
support for macro substitutions

From the EPICS Application Developer's Guide

:see: http://www.aps.anl.gov/epics/base/R3-14/12-docs/AppDevGuide/node7.html

    6.3.2 Unquoted Strings
    
    In the summary section, some values are shown as quoted strings and some unquoted. 
    The actual rule is that any string consisting of only the following characters 
    does not have to be quoted unless it contains one of the above keywords:
    
    ::

        a-z A-Z 0-9 _ -- : . [ ] < > ;
    
    ::

        my regexp:  [\w_\-:.[\]<>;]+([.][A-Z0-9]+)?
    
    These are also the legal characters for process variable names. 
    Thus in many cases quotes are not needed.
    
    6.3.3 Quoted Strings
    
    A quoted string can contain any ascii character except the quote character ". 
    The quote character itself can given by using \ as an escape. 
    For example "\"" is a quoted string containing the single character ".
    
    6.3.4 Macro Substitution
    
    Macro substitutions are permitted inside quoted strings.
    Macro instances take the form:
    
    ::

        $(name)
    
    or
    
    ::

        ${name}
    
    There is no distinction between the use of parentheses or braces 
    for delimiters, although the two must match for a given macro instance. 
    The macro name can be made up from other macros, for example:
    
    ::

        $(name_$(sel))
    
    A macro instance can also provide a default value that is used when no 
    macro with the given name is defined. The default value can be defined 
    in terms of other macros if desired, but cannot contain any unescaped 
    comma characters. The syntax for specifying a default value is as follows:
    
    ::

        $(name=default)
    
    Finally macro instances can also contain definitions of other macros, 
    which can (temporarily) override any existing values for those macros 
    but are in scope only for the duration of the expansion of this macro 
    instance. These definitions consist of name=value sequences separated 
    by commas, for example:
    
    ::
    
        $(abcd=$(a)$(b)$(c)$(d),a=A,b=B,c=C,d=D)


'''

import re

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# regular expression catalog

# a-z A-Z 0-9 _ -- : . [ ] < > ;
EPICS_UNQUOTED_STRING_RE = r'[\d\w_:;.<>\-\[\],]+'
EPICS_MACRO_SPECIFICATION_P_RE = "\$\("+EPICS_UNQUOTED_STRING_RE+"\)"       # _P_: parentheses
EPICS_MACRO_SPECIFICATION_B_RE = "\$\{"+EPICS_UNQUOTED_STRING_RE+"\}"       # _B_: braces
# EPICS_MACRO_DEFAULT_RE cannot find $(P=$(S)), that's OK.
# If the inner $(S) was expanded, it would be found then, else macro expansion fails anyway
EPICS_MACRO_DEFAULT_RE = EPICS_UNQUOTED_STRING_RE+'='+EPICS_UNQUOTED_STRING_RE
EPICS_MACRO_SPECIFICATION_PD_RE = "\$\("+EPICS_MACRO_DEFAULT_RE+"\)"
EPICS_MACRO_SPECIFICATION_BD_RE = "\$\{"+EPICS_MACRO_DEFAULT_RE+"\}"

EPICS_UNQUOTED_STRING_PATTERN = re.compile(EPICS_UNQUOTED_STRING_RE, 0)
EPICS_MACRO_SPECIFICATION_P_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_P_RE, 0)
EPICS_MACRO_SPECIFICATION_B_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_B_RE, 0)
EPICS_MACRO_DEFAULT_PATTERN = re.compile(EPICS_MACRO_DEFAULT_RE, 0)
EPICS_MACRO_SPECIFICATION_PD_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_PD_RE, 0)
EPICS_MACRO_SPECIFICATION_BD_PATTERN = re.compile(EPICS_MACRO_SPECIFICATION_BD_RE, 0)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Macros(object):
    '''manage a set of macros (keys, substitutions)'''
     
    def __init__(self, **env):
        self.db = {}
        self.setMany(**env)
    
    def __str__(self):
        return ', '.join([k+'="'+str(v)+'"' for k, v in sorted(self.items())])
            
    
    def exists(self, key):
        '''is there such a *key*?'''
        return key in self.db
    
    def get(self, key, missing=None):
        '''find the *key* macro, if not found, return *missing*'''
        return self.db.get(key, missing)
    
    def set(self, key, value, parent=None, ref=None):
        '''define the *key* macro'''
        self.db[key] = KVpair(parent, key, value, ref)
    
    def setMany(self, **env):
        '''define several macros'''
        self.db = dict(self.db.items() + env.items())
    
    def keys(self):
        '''get the list of macros, like dictionary.keys()'''
        return self.db.keys()
    
    def items(self):
        '''get the full database, like dictionary.items()'''
        return self.db.items()
    
    def replace(self, text):
        '''Replace macro parameters in source string'''
        return _replace_(text, self.db)


class KVpair(object):
    '''
    any *single* defined key:value pair in an EPICS IOC command file
    
    * PV field
    * Record field
    * Macro
    * Symbol
    '''

    def __init__(self, parent, key, value, ref=None):
        self.parent = parent
        self.key = key
        self.value = value
        self.reference = ref
    
    def __str__(self):
        return self.key + ' = ' + str(self.value)


def _replace_(source, macro_dict):
    '''
    Replace macro parameters in source string.
    Search through the dictionary of macros since there 
    may not be enough macros defined for all the 
    substitution patterns given.

    :param source: string with possible macro replacements
    :param macro_dict: dictionary of macro substitutions
    :return: string with substitutions applied
    :raise Exception: incorrect number of regular expression matches found
    '''
    if isinstance(source, KVpair):
        source = source.value   # TODO: is this ALWAYS true?
    last = ''
    while last != source:     # repeat to expand nested macros
        last = source
        # substitute the simple macro replacements
        for subst_marker in identifyEpicsMacros(source):
            parts = re.findall(EPICS_UNQUOTED_STRING_PATTERN, subst_marker, 0)
            if len(parts) == 1 and parts[0].find(','):
                parts = parts[0].split(',')
            if len(parts) == 1:
                # substitute the simple macros
                if parts[0] in macro_dict:
                    replacement_text = macro_dict[parts[0]]
                    if isinstance(replacement_text, KVpair):
                        replacement_text = replacement_text.value
                    source = source.replace(subst_marker, replacement_text)
            elif len(parts) == 2:
                # substitute the macros with default expressions
                macro_variable, default_substitution = parts
                if macro_variable in macro_dict:
                    replacement_text = macro_dict[macro_variable]
                    if isinstance(replacement_text, KVpair):
                        replacement_text = replacement_text.value
                    replacement_text = macro_dict[macro_variable].value
                else:
                    replacement_text = default_substitution
                source = source.replace(subst_marker, replacement_text)
            else:
                # add more diagnostics if this happens
                raise Exception, "should only match 1 or 2 parts here"
    return source


def identifyEpicsMacros(source):
    '''
    Identify any EPICS macro substitutions in the source string.
    Multiple entries of the same substitution (redundancies)
    are ignored.  Does not include nested macros such as:
    
    ::

        $(P=$(S))${S_$(P)}
        $(PJ=$(P))${S_$(P)}

    For these, only the innermost are returned:
    
    ::

        ['$(S)', '$(P)']
        ['$(P)']

    :note: This routine will also properly identify command shell macro substitutions.

    :param source: string with possible (EPICS) macro substitution expressions
    :return: list of macro substitutions found
    '''
    parts = []
    for patt in (EPICS_MACRO_SPECIFICATION_P_PATTERN, 
                 EPICS_MACRO_SPECIFICATION_B_PATTERN):
        for subst_marker in re.findall(patt, source, 0):
            if subst_marker not in parts:
                parts.append( subst_marker )
    for patt in (EPICS_MACRO_SPECIFICATION_PD_PATTERN, 
                 EPICS_MACRO_SPECIFICATION_BD_PATTERN):
        for subst_marker in re.findall(patt, source, 0):
            parts.append( subst_marker )
    return parts
