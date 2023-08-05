import json
import os
import base64

class Secrets:
    class SecretsError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
    def __init__(self, secrets_file):
        self.config = None
        if os.path.isfile(secrets_file) and os.access(secrets_file, os.R_OK):
            f = open(secrets_file).read()
            self.config = json.loads(f)
            if not self.validate_secrets():
                self.config = None
                raise self.SecretsError('Secrets not valid')
        else:
            raise IOError('Count not access secrets file')
    def dsn(self):
            return "dbname=" + self.config['database']['dbname'] + \
                " host=" + self.config['database']['host'] + \
                " user=" + self.config['database']['username'] + \
                " password=" + self.config['database']['password'] + \
                " port=" + str(self.config['database']['port'])
    def dhis(self):
        return self.config['dhis']
    def database(self):
        return self.config['database']
    def credentials(self):
        return (self.config['dhis']['username'], self.config['dhis']['password'])
    def get_auth_header(self):
        return base64.encodestring('%s:%s' % (self.config['dhis']['username'], self.config['dhis']['password'])).replace('\n', '')
    def validate_secrets(self):
        secrets_keys=['dhis', 'database']
        secrets_dhis = ['username', 'password', 'baseurl']
        secrets_database = ['username', 'host', 'password', 'port', 'dbname']
        return all([sorted(self.config.keys()) == sorted(secrets_keys), \
                    sorted(self.config['dhis'].keys())  == sorted(secrets_dhis), \
                    sorted(self.config['database'].keys())  == sorted(secrets_database)])