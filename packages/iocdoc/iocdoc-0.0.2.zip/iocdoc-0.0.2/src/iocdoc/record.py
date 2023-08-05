'''
EPICS record
'''

import macros


class RecordException(Exception): pass


class Record(object):
    '''definition of an EPICS record, macros are not expanded'''
     
    def __init__(self, parent, rtype, rname, ref, **env):
        self.parent = parent
        self.RTYP = rtype
        self.rname = rname
        self.macros = macros.Macros(**env)
        self.fields = dict(RTYP=rtype, NAME=rname)
        self.reference = ref
        self.alias_list = []
        self.info_dict = {}
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + self.rname
    
    def addFieldPattern(self, field, value, parent=None, ref=None):
        self.fields[field] = macros.KVpair(parent, field, value, ref)
    
    def addAlias(self, alias, parent=None, ref=None):
        self.alias_list.append(alias)   # TODO: what about a reference?
    
    def addInfo(self, key, field_list, parent=None, ref=None):
        self.info_dict[key] = macros.KVpair(parent, key, field_list, ref)


class PV(object):
    '''single instance of an EPICS record, will expand all macros as provided'''
     
    def __init__(self, record_object, ref, **env):
        self.record = record_object
        self.RTYP = record_object.RTYP
        self.macros = macros.Macros(**env)
        self.reference = ref

        self.fields = {k: self.macros.replace(v) for k, v in self.record.fields.items()}
        
        self.NAME = self.fields['NAME']
    
    def __str__(self):
        return 'record ' + self.RTYP + '  ' + str(self.macros.db)
    
    def getField(self, field, default=None):
        return self.fields[field]
    
    def getFields(self):
        return self.fields.items()
    
    def getFieldList(self):
        return self.fields.keys()
