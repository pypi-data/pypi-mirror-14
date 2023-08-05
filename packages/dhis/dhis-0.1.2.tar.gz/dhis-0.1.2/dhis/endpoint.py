class Endpoint:
    def __init__(self, info, server=None):
        self.name = None
        self.info = info
        self.server = server
        self.method = "GET"
        self.params = None
        self.return_type = None
        for item in info.items():
            setattr(self, item[0], item[1])
        if not self.return_type and self.relpath and self.relpath.endswith('json'):
            self.return_type = 'json'
        elif not self.return_type:
            self.return_type='text'
    def __repr__(self):
        if self.name:
            return '<Endpoint %s>' % self.name
        else:
            return '<Endpoint ' + str(self.info) + '>'
    def __str__(self):
        if self.name:
            return '<Endpoint %s>' % self.name
        else:
            return '<Endpoint ' + str(self.info) + '>'
