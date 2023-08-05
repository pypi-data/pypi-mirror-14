'''
EPICS IOC command file analysis
'''

import os
import token
import tokenize
import traceback


import database
import macros
import reports
import template
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions, reconstruct_line
from utils import logMessage, FileRef, strip_quotes, strip_parentheses


class UnhandledTokenPattern(Exception): pass


class Command(object):
    '''
    one command in an EPICS IOC command file
    '''

    def __init__(self, parent, command, path, args, ref, **env):
        self.parent = parent
        self.command = command
        self.path = path
        self.args = args
        self.env = macros.Macros(**env)
        self.reference = ref
    
    def __str__(self):
        return self.command + ' ' + str(self.args) + ' ' + str(self.env)


class CommandFile(object):
    '''
    analysis of an EPICS IOC command file
    '''

    def __init__(self, parent, filename, ref, **env):
        self.parent = parent
        self.filename = filename
        self.reference = ref
        self.pwd = os.getcwd()      # TODO: needs some attention here

        self.env = macros.Macros(**env)
        self.symbols = macros.Macros()
        self.database_list = []
        self.commands = []
        self.template_list = []
        self.includedCommandFile_list = []
        self.pv_dict = {}

        # filename is a relative or absolute path to command file, no macros in the name
        self.filename_absolute = os.path.abspath(filename)
        self.dirname_absolute = os.path.dirname(self.filename_absolute)
        #self.filename_expanded = self.env.replace(filename)
        self.source = text_file.read(filename)

        self.knownHandlers = {
            '<': self.kh_loadCommandFile,
            'cd': self.kh_cd,
            # 'dbLoadDatabase': self.kh_dbLoadDatabase,
            'dbLoadRecords': self.kh_dbLoadRecords,
            'dbLoadTemplate': self.kh_dbLoadTemplate,
            'epicsEnvSet': self.kh_epicsEnvSet,
            'putenv': self.kh_putenv,
            # 'seq': self.kh_seq,
            'strcpy': self.kh_strcpy,
            # 'nfsMount': self.kh_nfsMount,
            # 'nfs2Mount': self.kh_nfsMount,
            #------ overrides -----------
            'dbLoadDatabase': self.kh_shell_command,
            'seq': self.kh_shell_command,
            'nfsMount': self.kh_shell_command,
            'nfs2Mount': self.kh_shell_command,
        }
        self.parse()
    
    def __str__(self):
        return str(self.reference) + ' ' + self.filename
    
    def _make_ref(self, tok, item=None):
        '''make a FileRef() instance for this item'''
        return FileRef(self.filename, tok['start'][0], tok['start'][1], item or self)
    
    def parse(self):
        '''analyze this command file'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename)
        lines = tokenLog.lineAnalysis()
        del lines['numbers']
        for _lineNumber, line in sorted(lines.items()):
            isNamePattern = line['pattern'].startswith( 'NAME' )
            tk = token_key(line['tokens'][0])
            if isNamePattern or tk == 'OP <':
                arg0 = line['tokens'][0]['tokStr']
                ref = self._make_ref(line['tokens'][0], arg0)
                if line['tokens'][1]['tokStr'] == '=':
                    # this is a symbol assignment
                    handler = self.kh_symbol
                    handler(arg0, line['tokens'], ref)
                elif arg0 in self.knownHandlers:
                    # command arg0 has a known handler, call it
                    handler = self.knownHandlers[arg0]
                    handler(arg0, line['tokens'], ref)
                else:
                    self.kh_shell_command(arg0, line['tokens'], ref)

    def kh_cd(self, arg0, tokens, ref):
        path = reconstruct_line(tokens).strip()
        if self.symbols.exists(path):       # symbol substitution
            path = self.symbols.get(path).value
        path = self.env.replace(path)       # macro substitution
        path = strip_quotes(path)           # strip double-quotes
        if len(path) > 0 and os.path.exists(path):
            os.chdir(path)
            self.kh_shell_command(arg0, tokens, ref)

    def kh_dbLoadRecords(self, arg0, tokens, ref):
        local_macros = macros.Macros(**self.env.db)
        tokenLog = TokenLog()
        tokenLog.tokenList = tokens
        tokenLog.token_pointer = 1
        parts = parse_bracketed_macro_definitions(tokenLog)
        count = len(parts)
        if count == 0 or count > 3:
            msg = str(ref) + reconstruct_line(tokens).strip()
            raise UnhandledTokenPattern, msg
        if count > 0:
            dbFileName = strip_quotes(parts[0])
        if count > 1:
            for definition in strip_quotes(parts[1]).split(','):
                k, v = definition.split('=')
                local_macros.set(k, v, self, ref)
        # TODO: distinguish between environment macros and new macros for this instance
        if count == 3:
            path = parts[2]
            msg = str(ref) + reconstruct_line(tokens).strip()
            # TODO: how to handle this?
            raise UnhandledTokenPattern, msg
        try:
            obj = database.Database(self, dbFileName, ref, **local_macros.db)
            self.database_list.append(obj)
            self.kh_shell_command(arg0, tokens, ref)
        except text_file.FileNotFound, _exc:
            # TODO: what to do at this point?  Need report and continue mechanism
            traceback.print_exc()
            return
        for k, v in obj.getPVs():
            self.pv_dict[k] = v

    def kh_dbLoadTemplate(self, arg0, tokens, ref):
        local_macros = macros.Macros(**self.env.db)
        tfile = strip_quotes(strip_parentheses(reconstruct_line(tokens).strip()))
        obj = template.Template(tfile, ref, **local_macros.db)
        self.template_list.append(obj)
        # TODO: anything else to be done?
        self.kh_shell_command(arg0, tokens, ref)
        for k, v in obj.getPVs():
            self.pv_dict[k] = v

    def kh_epicsEnvSet(self, arg0, tokens, ref):
        '''symbol assignment'''
        if len(tokens) == 7:
            var = tokens[2]['tokStr']
            value = tokens[4]['tokStr']
        else:
            text = strip_parentheses(reconstruct_line(tokens).strip())
            parts = text.split(',')
            if len(parts) == 1:
                parts = text.split(' ')
            if len(parts) != 2:
                raise UnhandledTokenPattern('epicsEnvSet'+text)
            var, value = parts
        self.env.set(strip_quotes( var ), strip_quotes( value ), self, ref)
        self.kh_shell_command(arg0, tokens, ref)

    def kh_loadCommandFile(self, arg0, tokens, ref):
        fname = strip_parentheses(reconstruct_line(tokens).strip())
        # fname is given relative to current working directory
        fname_expanded = self.env.replace(fname)
        obj = CommandFile(self, fname_expanded, ref, **self.env.db)
        self.includedCommandFile_list.append(obj)
        self.kh_shell_command('<', tokens, ref)

        self.commands += obj.commands
        self.symbols.setMany(**obj.symbols.db)
        self.env.setMany(**obj.env.db)
        for k, v in obj.pv_dict.items():
            self.pv_dict[k] = v

    def kh_putenv(self, arg0, tokens, ref):
        '''
        process an instance of putenv

        :param tokens: token list
        :param ref: instance of :class:`iocdoc.utils.FileRef`
        :raise UnhandledTokenPattern: unhandled token pattern
        '''
        argument_list = []
        for tkn in tokens[1:]:
            if tkn['tokName'] == 'STRING':
                argument_list.append( tkn['tokStr'] )

        if len(argument_list) == 1:
            var, arg = strip_quotes( argument_list[0].strip() ).split('=')
            arg = strip_quotes(arg.strip())
            self.env.set(var, arg, self, ref)
        elif len(argument_list) == 2:
            var, arg = argument_list
            arg = strip_quotes(arg.strip())
            self.env.set(var, arg)
        else:
            msg = str(ref) + reconstruct_line(tokens).strip()
            raise UnhandledTokenPattern, msg

        self.kh_shell_command(arg0, tokens, ref)

    def kh_shell_command(self, arg0, tokens, ref):
        linetext = reconstruct_line(tokens).strip()
        cmd = Command(self, arg0, self.pwd, linetext, ref, **self.env.db)
        self.commands.append(cmd)

    def kh_strcpy(self, arg0, tokens, ref):
        '''symbol assignment'''
        self.kh_symbol(arg0, tokens, ref)

    def kh_symbol(self, arg0, tokens, ref):
        '''symbol assignment'''
        arg = strip_quotes( tokens[2]['tokStr'] )
        obj = macros.KVpair(self, arg0, arg, ref)
        self.symbols.set(arg0, obj, self, ref)
        self.kh_shell_command('(symbol)', tokens, ref)


def main():
    owd = os.getcwd()
    cmdFile_dict = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'iocBoot', 'ioc495idc', 'st.cmd'))
    IOC_NAME = 'testing'
    env = {}
    for i, tf in enumerate(testfiles):
        try:
            os.chdir(os.path.dirname(os.path.abspath(tf)))
            ref = FileRef(__file__, i, 0, 'testing')
            cmdFile_object = CommandFile(None, os.path.split(tf)[-1], ref, **env)
        except Exception:
            traceback.print_exc()
            continue
        cmdFile_dict[tf] = cmdFile_object
        
        os.chdir(owd)
        reports.reportCmdFile(cmdFile_object, IOC_NAME)


if __name__ == '__main__':
    main()
