import json, os, urllib
from urllib.parse import urlparse
from urllib.request import urlopen
from dhis.configuration import Configuration

class Config:
    def __init__(self, location=None, profile=None):
        abspath=os.path.abspath("dhis2conf.json")
        homepath=os.path.abspath(os.path.expanduser("~/.dhis2conf.json"))
        self.config = None
        self.type = None
        self.profile = profile
        if location:
            if urlparse(location).scheme:
                self.type = 'url'
            else:
                fullpath=os.path.abspath(location)
                if (os.path.isfile(fullpath)) and os.access(fullpath, os.R_OK):
                    self.type = 'file'
                else:
                    raise Exception('Config could not be read.')
        elif ((os.path.isfile(abspath)) and os.access(abspath, os.R_OK)):
            location = abspath
            self.type = 'file'
        elif (os.path.isfile(homepath)) and os.access(homepath, os.R_OK):
            location = homepath
            self.type = 'file'
        else:
            self.type = 'sysenv'
        if location:
            print('Loading '+self.type+'config from ' + location, end='\n', flush=True)
        if self.type:
            if self.type == 'url':
                loaded = json.loads(urlopen(location).read())
            elif self.type == 'file':
                loaded = json.loads(open(location).read())
            else:
                dbconfig = {}
                apiconfig = {}
                dbconfig['host'] = os.getenv("DHIS2DB_HOST")
                dbconfig['port'] = os.getenv("DHIS2DB_PORT")
                dbconfig['username'] = os.getenv("DHIS2DB_USER")
                dbconfig['password'] = os.getenv("DHIS2DB_PASSWORD")
                dbconfig['database'] = os.getenv("DHIS2DB_DBNAME")
                apiconfig['baseurl'] = os.getenv("DHIS2API_ROOT")
                apiconfig['username'] = os.getenv("DHIS2API_USER")
                apiconfig['password'] = os.getenv("DHIS2API_PASSWORD")
                loaded = {'database': Configuration(dbconfig),
                          'dhis': Configuration(apiconfig)}
        if loaded.get('database') or loaded.get('dhis'):
            for item in loaded.items():
                if type(item[1]) is not str:
                    loaded[item[0]] = Configuration(item[1])
                    self.config = loaded
                elif loaded.get('dbname'):
                    self.config = {'database': Configuration(loaded['database'])}
                elif loaded.get('baseurl'):
                    self.config = {'dhis': Configuration(loaded['dhis'])}
                else:
                    raise Exception('odd config', loaded)
        else:
            raise Exception('No suitable configuration could be found')
    def resolve_config(self, config, base):
        probe = base
        while probe and (type(probe) is str):
            probe = config.get(probe)
        if probe:
            return probe
        else:
            return config
    def getconfig(self, url=None):
        config = self.config
        if url:
            parsed = urlparse(url)
            probe = url
            if (config.get(probe)):
                return self.resolve_config(config, probe)
            if parsed.port:
                probe = '%s:%d' % (parsed.hostname, parsed.port)
            else:
                probe = '%s:80' % parsed.hostname
            if (config.get(probe)):
                return self.resolve_config(config, probe)
            probe = parsed.hostname
            if (config.get(probe)):
                return self.resolve_config(config, probe)
            elif self.profile and config.get(self.profile):
                return self.resolve_config(config, self.profile)
            elif (parsed.scheme == 'http' or parsed.scheme == 'https'):
                if (config.get('dhis')):
                    return self.resolve_config(config, 'dhis')
                else:
                    return config
            else:
                return config
        elif self.profile and config.get(self.profile):
            return self.resolve_config(config, self.profile)
        elif (config.get('database')):
            return self.resolve_config(config, 'database')
        elif (config.get('dhis')):
            return self.resolve_config(config, 'dhis')
        else:
            return config
    def dsn(self):
            return "dbname=" + self.getconfig('database').dbname + \
                " host=" + self.getconfig('database').host + \
                " user=" + self.getconfig('database').username + \
                " password=" + self.getconfig('database').password + \
                " port=" + str(self.getconfig('database').port)
