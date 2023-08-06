
import os, re, time
from configparser import ConfigParser, ExtendedInterpolation
from bl.dict import Dict         # needed for dot-attribute notation

LIST_PATTERN = "^\[\s*([^,]*)\s*(,\s*[^,]*)*,?\s*\]$"
DICT_ELEM = """(\s*['"].+['"]\s*:\s*[^,]+)"""
DICT_PATTERN = """^\{\s*(%s,\s*%s*)?,?\s*\}$""" % (DICT_ELEM, DICT_ELEM)

class Config(Dict):
    """class for holding application configuration in an Ini file. Sample Usage:
    >>> cf_filename = os.path.join(os.path.dirname(__file__), "config_test.ini")
    >>> cf = Config(cf_filename)
    >>> cf.Archive.path             # basic string conversion
    '/data/files'
    >>> cf.Test.debug               # boolean 
    True
    >>> cf.Test.list                # list with several types
    [1, 2, 'three', True, 4.0]
    >>> cf.Test.dict                # dict => Dict
    {'a': 1, 'b': 'two', 'c': False}
    >>> cf.Test.dict.a              # Dict uses dot-notation
    1
    """

    def __init__(self, filename, interpolation=ExtendedInterpolation(), 
                split_list=None, join_list=None, **kwargs):
        config = ConfigParser(interpolation=interpolation, **kwargs)
        self.__dict__['__filename__'] = filename
        self.__dict__['__join_list__'] = join_list
        if config.read(filename):
            self.parse_config(config, split_list=split_list)
        else:
            raise KeyError("Config file not found at %s" % filename)

    def __repr__(self):
        return "Config('%s')" % self.__filename__

    def parse_config(self, config, split_list=None):
        for s in config.sections():
            self[s] = Dict()
            for k, v in config.items(s):
                # resolve common data types
                if v.lower() in ['true', 'false', 'yes', 'no']:     # boolean
                    self[s][k] = config.getboolean(s, k)
                elif re.match("^\-?\d+$", v):                       # integer
                    self[s][k] = int(v)
                elif re.match("^\-?\d+\.\d*$", v):                  # float
                    self[s][k] = float(v)
                elif re.match(LIST_PATTERN, v):                     # list
                    self[s][k] = eval(v)
                elif re.match(DICT_PATTERN, v):                     # dict
                    self[s][k] = Dict(**eval(v))
                elif split_list is not None \
                and re.search(split_list, v) is not None:
                    self[s][k] = re.split(split_list, v)
                else:                                               # default: string
                    self[s][k] = v.strip()

    def write(self, fn=None, sorted=False, wait=0):
        """write the contents of this config to fn or its __filename__.
        NOTE: All interpolations will be expanded in the written file.
        """
        config = ConfigParser(interpolation=None)
        keys = self.keys()
        if sorted==True: keys.sort()
        for key in keys:
            config[key] = {}
            ks = self[key].keys()
            if sorted==True: ks.sort()
            for k in ks:
                if type(self[key][k])==list and self.__join_list__ is not None:
                    config[key][k] = self.__join_list__.join([v for v in self[key][k] if v!=''])
                else:
                    config[key][k] = str(self[key][k])
        print(fn, self.__dict__.get('__filename__'))
        fn = fn or self.__dict__.get('__filename__')
        # use advisory locking on this file
        i = 0
        while os.path.exists(fn+'.LOCK') and i < wait:
            i += 1
            time.sleep(1)
        if os.path.exists(fn+'.LOCK'):
            raise FileExistsError(fn + ' is locked for writing')
        else:
            with open(fn+'.LOCK', 'w') as lf:
                lf.write(time.strftime("%Y-%m-%d %H:%M:%S %Z"))
            with open(fn, 'w') as f:
                config.write(f)
            os.remove(fn+'.LOCK')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
