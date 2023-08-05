class Configuration:
    def __init__(self, configdata):
        self.name = None
        self.configdata = configdata
        self.username = ''
        self.password = ''
        if configdata.get('baseurl'):
            self.kind = 'dhis'
        elif configdata.get('dbname'):
            self.kind = 'database'
        else:
            self.kind = None
        if self.kind == "database":
            self.port = None
            self.hostname = 'localhost'
        if self.kind == 'dhis':
            self.baseurl = None
        for item in configdata.items():
            setattr(self, item[0], item[1])
    def __repr__(self):
        if self.kind and self.name:
            return '<%s configuration %s>' % (self.kind, self.name)
        elif self.name:
            return '<Configuration %s>' % self.name
        elif (self.kind == 'API'):
            return '<API configuration for %s@%s>' % (self.username, self.baseurl)
        elif (self.kind == 'Database'):
            return '<DB configuration for %s@%s:%s as %s>' % (self.dbname, self.hostname, self.port, self.username)
        elif (self.kind):
            return '<%s configuration %s>' % (self.kind, str(self.configdata))
        else:
            return '<Configuration ' + str(self.configdata) + '>'
    def __str__(self):
        if self.kind:
            return '<%s configuration %s>' % (self.kind, str(self.configdata))
        else:
            return '<Configuration %s>' % str(self.configdata)
