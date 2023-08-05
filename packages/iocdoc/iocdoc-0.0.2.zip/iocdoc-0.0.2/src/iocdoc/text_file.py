'''
text_file.py - describe any text file used by an EPICS IOC

======================== ====================================================
code                     description
======================== ====================================================
:func:`read`             get a file either from the cache or from storage
:func:`items`            get the cache as a set of dictionary items
:func:`keys`             get the names of files in the cache
:func:`values`           get the Python objects of items in the cache
:func:`remove_comments`  strip out a C-style comment
:exc:`FileNotFound`      Exception: raised when ``filename`` does not exist
:class:`_FileCache`      (internal) supports "load each file only once"
:class:`_TextFile`       (internal) superclass: common handling of text file
======================== ====================================================

Example::

    # filename must have all macros expanded
    file_object = text_file.read(filename)


'''


import os
import StringIO


class FileNotFound(Exception): pass


_file_cache_ = None       # (internal) singleton instance of FileCache()


def read(filename):
    '''
    get a file either from the cache or from storage
    
    :param str filename: relative or absolute path to file
    
    Always use filenames with all macros expanded.
    
    ====== ===========================================
    Ok?    filename
    ====== ===========================================
    Ok     ``st.cmd``
    Ok     ``./testfiles/templates/example.template``
    not Ok ``$(SSCAN)/sscanApp/Db/scanParms.db``
    ====== ===========================================
    '''
    global _file_cache_
    if _file_cache_ is None:
        _setup_file_cache()
    #filename = os.path.abspath(filename)
    if not _file_cache_.exists(filename):
        _file_cache_.set(filename, _TextFile(filename))
    return _file_cache_.get(filename)


def items():
    '''get the cache as a set of dictionary items'''
    return _file_cache_.cache.items()


def keys():
    '''get the names of files in the cache'''
    return _file_cache_.cache.keys()


def values():
    '''get the Python objects of items in the cache'''
    return _file_cache_.cache.values()


# --- internal routines below --------------


def _setup_file_cache():
    '''define ``_file_cache_`` as a singleton'''
    global _file_cache_
    _file_cache_ = _FileCache()


class _FileCache(object):
    '''load each file only once'''
    
    def __init__(self):
        global _file_cache_
        if _file_cache_ is not None:
            msg = '_FileCache() called more than once'
            msg += ': use text_file._file_cache_ object instead'
            raise RuntimeError(msg)
        self.cache = {}
        _file_cache_ = self
    
    def exists(self, filename):
        return filename in self.cache
    
    def set(self, filename, value):
        '''
        define a reference to a file in the cache
        '''
        self.cache[filename] = value
    
    def get(self, filename, alternative = None):
        '''
        get a reference to a file from the cache
        '''
        return self.cache.get(filename, alternative)


class _TextFile(object):
    '''
    superclass: description and common handling of a text file used by this package
    
    This class should only be called by the read() method above.
    '''
    
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            _pwd = os.getcwd()  # for diagnostic purposes in the debugger
            raise FileNotFound(filename)

        self.absolute_filename = os.path.abspath(filename)
        self.absolute_directory = os.path.dirname(self.absolute_filename)
        stats = os.stat(self.absolute_filename)
        self.mtime = stats.st_mtime 
        self.bytes = stats.st_size 
        self.cwd = os.getcwd()

        self._read()
        self.number_of_lines = len(self)
    
    def close(self):
        '''some code likes to call this'''
        pass
    
    def iterator(self):
        '''iterator interface: provide str.readline for tokenizer'''
        return StringIO.StringIO(self.full_text)
    
    def __len__(self):
        '''iterator interface'''
        return len(self.full_text.splitlines())
    
    def _read(self):
        '''read the complete file from storage'''
        if not os.path.exists(self.absolute_filename):
            raise FileNotFound(self.absolute_filename)
        self.full_text = open(self.absolute_filename, 'r').read()
    
    def __str__(self):
        return self.filename
