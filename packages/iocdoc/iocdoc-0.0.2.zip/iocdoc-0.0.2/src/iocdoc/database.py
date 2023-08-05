'''
EPICS database file analysis
'''

import os
import macros
import record
import text_file
from token_support import token_key, TokenLog, parse_bracketed_macro_definitions
from utils import logMessage, FileRef


class DatabaseException(Exception): pass


class Database(object):
    '''
    call for one EPICS database file with a given environment
    '''
     
    def __init__(self, parent, dbFileName, ref, **env):
        # TODO: distinguish between environment macros and new macros for this instance
        self.parent = parent
        self.filename = dbFileName
        self.macros = macros.Macros(**env)
        self.filename_expanded = self.macros.replace(dbFileName)
        self.record_list = None
        self.pv_dict = {}
        self.reference = ref

        # read the file (if the first time, parse its content)
        self.source = text_file.read(self.filename_expanded)
        if not hasattr(self.source, 'record_list'):
            self.source.record_list = []
            self.record_list = self.source.record_list
            self.parse()    # step 1: parse the db file for its definitions
        self.record_list = self.source.record_list

        # apply supplied macros for each call to the database file
        self.makeProcessVariables()
    
    def __str__(self):
        return 'dbLoadRecords ' + self.filename + '  ' + str(self.macros)
    
    def _make_ref(self, tok, item=None):
        '''make a FileRef() instance for this item'''
        return FileRef(self.filename, tok['start'][0], tok['start'][1], item or self)
    
    def makeProcessVariables(self):
        '''make the EPICS PVs from the record definitions'''
        # build self.pv_dict from self.record_list and self.macros
        if self.record_list is None:
            print self.filename
            print len(self.record_list)
        for rec in self.record_list:
            ref = rec.reference
            ref.filename = self.filename
            ref.object = self
            pv = record.PV(rec, ref, **self.macros.db)
            self.pv_dict[pv.NAME] = pv
            for alias in rec.alias_list:
                alias_expanded = self.macros.replace(alias)
                if alias_expanded not in self.pv_dict:
                    self.pv_dict[alias_expanded] = pv
     
    def parse(self):
        '''interpret records for PV declarations'''
        tokenLog = TokenLog()
        tokenLog.processFile(self.filename_expanded)
        tok = tokenLog.nextActionable()
        actions = {
                   #'NAME alias': self._parse_alias,
                   #'NAME info': self._parse_info,
                   'NAME grecord': self._parse_record,
                   'NAME record': self._parse_record,
                   }
        while tok is not None:
            tk = token_key(tok)
            if tk in actions:
                actions[tk](tokenLog)
            tok = tokenLog.nextActionable()
    
    def _parse_record(self, tokenLog):
        tok = tokenLog.nextActionable()
        ref = self._make_ref(tok)
        rtype, rname = tokenLog.tokens_to_list()
        # just parsing, no need for macros now
        record_object = record.Record(self, rtype, rname, ref)
        self.record_list.append(record_object)

        tok = tokenLog.nextActionable()
        if token_key(tok) == 'OP {':
            tok = tokenLog.nextActionable()
            # get record's field definitions
            while token_key(tok) != 'OP }':
                ref = self._make_ref(tok, tok['tokStr'])
                if token_key(tok) == 'NAME field':
                    tok = tokenLog.nextActionable()
                    ref = self._make_ref(tok)
                    field, value = parse_bracketed_macro_definitions(tokenLog)
                    record_object.addFieldPattern(field, value.strip('"'), self, ref)
                    tok = tokenLog.previous()   # backup before advancing below
                elif token_key(tok) == 'NAME alias':
                    self._parse_alias(tokenLog, record_object, ref)
                elif token_key(tok) == 'NAME info':
                    self._parse_info(tokenLog, record_object, ref)
                else:
                    tok = tokenLog.getCurrentToken()
                    msg = str(ref) + ' unexpected content: |%s|' % str(tok['tokStr'])
                    raise RuntimeError(msg)
                tok = tokenLog.nextActionable()
    
    def _parse_info(self, tokenLog, record_object, ref):
        tok = tokenLog.nextActionable()
        ref = self._make_ref(tok, 'database "info" command')
        parts = tokenLog.tokens_to_list()
        if len(parts) != 2:
            msg = str(ref) + ' ' + str(parts)
            raise DatabaseException, msg
        key = parts[0]
        field_list = parts[1].split(' ')
        record_object.addInfo(key, field_list, self, ref)
    
    def _parse_alias(self, tokenLog, record_object, ref):
        tok = tokenLog.nextActionable()
        ref = self._make_ref(tok, 'database "alias" command')
        parts = tokenLog.tokens_to_list()
        if len(parts) != 1:
            msg = str(ref) + ' ' + str(parts)
            raise DatabaseException, msg
        alias = parts[0]
        record_object.addAlias(alias, self, ref)
     
    def getPVList(self):
        return self.pv_dict.keys()
     
    def getPVs(self):
        return self.pv_dict.items()


def main():
    db = {}
    testfiles = []
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'iocAdminVxWorks.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'pseudoMotor.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'Charlie'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'asynRecordAliases.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'autoShutter.vdb'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'filterBladeNoSensor.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'filterDrive.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'saveData.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'scan.db'))
    testfiles.append(os.path.join('.', 'testfiles', 'databases', 'scanParms.db'))
    macros = dict(TEST="./testfiles", P='prj:', M='m11')
    for i, tf in enumerate(testfiles):
        try:
            ref = FileRef(__file__, i, 0, 'testing')
            db[tf] = Database(None, tf, ref, **macros)
        except text_file.FileNotFound, _exc:
            print 'file not found: ' + tf
            continue
        except NotImplementedError, _exc:
            print 'Not implemented yet: ' + str(_exc)
            continue
        print db[tf]
        for k, pv in sorted(db[tf].getPVs()):
            print '\t%015s %s' % (pv.RTYP, k)


if __name__ == '__main__':
    main()
