
'''
generate the standard reports for *iocdoc*
'''

import os
import pyRestTable
import text_file


def reportCmdFile(obj, ioc_name='Command File'):
    '''report what was learned from the command file'''
    print mk_title('IOC: ' + ioc_name, '=')
    print 'initial startup command script file: ', obj
    print 'absolute path: ', obj.filename_absolute
    
    print '\n'
    print mk_title('Table: IOC Command sequence')
    print reportCommandSequence(obj.commands)
    
    print '\n'
    print mk_title('Table: EPICS Records types used')
    print reportRTYP(obj.pv_dict)
    
    print '\n'
    print mk_title('Table: EPICS IOC shell commands used')
    print reportCommandCount(obj.commands)
    
    print '\n'
    print mk_title('Table: EPICS Motor types used')
    print reportMotorCount(obj.pv_dict)
    
    # print '\n'
    # print mk_title('Table: Process Variables')
    # print reportPVs(obj.pv_dict)
            
    print '\n'
    print mk_title('Table: MACROS')
    # switch reportSymbols() once macros get an object reference
    # old: reportMacros()
    print reportSymbols(obj.env.db)
    
    print '\n'
    print mk_title('Table: SYMBOLS')
    print reportSymbols(obj.symbols.db)
    
    print '\n'
    print mk_title('Table: EPICS Databases')
    # TODO: obj.database_list is not *ALL* the databases
    print reportDatabases(obj.database_list)
    
    print '\n'
    print mk_title('Table: text file cache')
    print reportTextFiles()


def mk_title(text='title', symbol='-'):
    return '\n'.join( [text, symbol*len(text), ''] )


def _makeCountTable(xref, label='subject'):
    '''show the xref table in a dict'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', label, 'count']
    count = 0
    i = 0
    for k, v in sorted(xref.items()):
        i += 1
        tbl.rows.append([i, k, v])
        count += v
    tbl.rows.append(['--', 'TOTAL', count])
    return tbl.reST()


def reportCommandCount(cmd_list):
    '''how many of each command?'''
    xref = {}
    for cmd in cmd_list:
        if cmd.command not in xref:
            xref[cmd.command] = 0
        xref[cmd.command] += 1
    return _makeCountTable(xref, label='command')


def reportCommandSequence(cmd_list):
    '''show the order of the commands'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'command', 'arguments']
    for i, command in enumerate(cmd_list):
        tbl.rows.append([i+1, command.reference, command.command, command.args])
    return tbl.reST()


def reportDatabases(db_list):
    '''show the databases that were used'''
    if len(db_list) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'database file']
    for i, db in enumerate(db_list):
        # TODO: distinguish between environment macros and new macros for this instance
        tbl.rows.append([i+1, db.reference, db.filename])
    return tbl.reST()


def reportMacros(macro_dict):
    '''Show the macros in a table'''
    if len(macro_dict) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', 'name', 'definition']
    i = 0
    for k, v in sorted(macro_dict.items()):
        i += 1
        tbl.rows.append([i, k, v])
    return tbl.reST()


def reportMotorCount(pv_dict):
    '''how many of each type of motor?'''
    xref = {}
    for k, pv in pv_dict.items():
        if pv.RTYP == 'motor' and k == pv.NAME:
            dtype = pv.getField('DTYP', 'undefined')
            if dtype == 'asynMotor':
                dtype += ' ' + pv.getField('OUT', '')
            if dtype not in xref:
                xref[dtype] = 0
            xref[dtype] += 1
    if len(xref) == 0:
        return 'no motors'
    return _makeCountTable(xref, label='motor type')


def reportPVs(pv_dict):
    '''List the defined process variables'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'record type', 'PV name']
    i = 0
    for _k, pv in sorted(pv_dict.items()):
        i += 1
        tbl.rows.append([i, pv.reference, pv.RTYP, pv.NAME])
    return tbl.reST()


def reportRTYP(pv_dict):
    '''how many of each record type?'''
    xref = {}
    for k, pv in pv_dict.items():
        if k != pv.NAME:
            rtype = 'alias'
        else:
            rtype = pv.RTYP
        if rtype not in xref:
            xref[rtype] = 0
        xref[rtype] += 1
    return _makeCountTable(xref, label='RTYP')


def reportSymbols(macro_dict):
    '''Show the symbols in a table'''
    if len(macro_dict) == 0:
        return 'none'
    tbl = pyRestTable.Table()
    tbl.labels = ['#', '(file_name,line,column)', 'name', 'value']
    i = 0
    for _k, v in sorted(macro_dict.items()):
        i += 1
        tbl.rows.append([i, v.reference, v.key, v.value])
    return tbl.reST()


def reportTextFiles():
    '''show the text files that were read'''
    tbl = pyRestTable.Table()
    tbl.labels = ['#', 'file_name', 'path']
    i = 0
    for _k, v in sorted(text_file.items()):
        i += 1
        tbl.rows.append([i, os.path.split(v.filename)[-1], v.absolute_filename])
    return tbl.reST()
