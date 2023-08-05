import base64, requests, json

from dhis.config import Config
from dhis.endpoint import Endpoint
from dhis.types.types import Generic
from urllib.parse import urlparse, urlunparse

class Server:
    def __init__(self, config=None, 
                 baseurl=None, 
                 username=None, 
                 password=None,
                 profile=None):
        if not config:
            config=Config()
        elif type(config) is not Config: 
            config=Config(config)
        else:
            config=config
        if not baseurl:
            baseurl = config.getconfig("dhis").baseurl
        if not baseurl:
            raise Exception('Server requires baseurl')
        elif type(baseurl) is not str:
            # Handle unparsed URLs as baseurls
            baseurl = urlunparse(baseurl)
        if not urlparse(baseurl).hostname:
            raise Exception('Bad baseurl arg', baseurl)
        if baseurl.endswith('/api/'):
            baseurl = baseurl
        elif baseurl.endswith('/'):
            baseurl += 'api/'
        else:
            baseurl = baseurl + '/api/'
        if not username:
            username = config.getconfig(baseurl).username
        if type(username) is not str:
            raise Exception('bad username', username)
        if not password:
            password = config.getconfig(baseurl).password
        if type(password) is not str:
            # Don't pass the password arg to try and keep it out of
            # error messages which anyone might see
            raise Exception('bad password')
        self.baseurl = baseurl
        self.username = username
        self.password = password
        self.credentials = (username, password)
        self.endpoints = {}
        self.config = config
        self.__cookies = None

    def get_auth_string(self):
        return base64.encodebytes('%s:%s' % (self.username, self.password)).replace('\n', '')

    def __sec(self,kwargs,headers):  # Add security, either username/password or cookie
        if self.__cookies:
            kwargs["cookies"] = self.__cookies
        else:
            kwargs["auth"] = self.credentials
        return headers

    def __out(self, result):  # First time: Grab security cookie for future calls
        if not self.__cookies and result.cookies and result.cookies["JSESSIONID"]:
            # print("saving JSESSIONID "+result.cookies["JSESSIONID"]+"on "+self+"\n")
            self.__cookies = {"JSESSIONID": result.cookies["JSESSIONID"]}
        return result

    wrapper_params = ['return_type', 'content-type', 'content-length','headers',
                      'content-encoding', 'date', 'host', 'auth','return_class']

    def call(self, endpoint, method=None, 
             return_type=None, return_class=None, 
             jsondata=None, params={}, headers={},
             **kwargs):
        auth = self.credentials
        headers = self.__sec(kwargs,headers)
        if not 'headers' in kwargs:
            kwargs['headers']=headers
        baseurl= self.baseurl
        if type(endpoint) is str:
            if endpoint.endswith('json') and not return_type:
                use_return_type = 'json'
            elif not return_type:
                use_return_type = 'request'
            else:
                use_return_type = return_type
            endpoint = Endpoint({'name': endpoint, 'relpath': endpoint,
                                 'method': method,
                                 'return_type': use_return_type,
                                 'return_class': return_class})
        if not method and endpoint.method:
            method = endpoint.method
        elif not method:
            method = "GET"
        path = baseurl + endpoint.relpath
        if not return_type:
            if endpoint.return_type:
                return_type = endpoint.return_type
        if endpoint.params:
            for arg in endpoint.params:
                params[arg] = kwargs.get(arg)
        else:
            for item in kwargs.items():
                if item[0] not in Server.wrapper_params:
                    params[item[0]] = item[1]
        if return_type in ['collection']:
            params['paging']=False

        if return_type in ['collection','object','json']:
            if not path.endswith('.json'):
                path=path+'.json'

        if jsondata:
            kwargs['data']=json.dumps(jsondata)
            headers['content-type']='application/json'

        # print('headers='+str(headers))

        if method == 'GET':
            result = requests.get(path, params=params, **kwargs)
        elif method == 'PUT':
            result = requests.put(path, params=params, **kwargs)
        elif method == 'POST':
            result = requests.post(path, params=params, **kwargs)
        elif method == 'PATCH':
            result = requests.patch(path, params=params, **kwargs)
        elif method == 'DELETE':
            result = requests.delete(path, params=params, **kwargs)
        else:
            result = requests.get(path, params=params, **kwargs)
        result = self.__out(result)
        if return_type == 'request':
            return result
        elif result.status_code != 200:
            raise Exception('HTTP error', result)
        elif not endpoint.return_type:
            return result
        elif endpoint.return_type == 'json':
            return result.json()
        elif endpoint.return_type == 'object':
            asjson=result.json()
            constructor=endpoint.return_class
            if not constructor:
                return Generic(asjson)
            else:
                return constructor(asjson)
        elif endpoint.return_type == 'collection':
            return self.getall(result.json())
        elif endpoint.return_type == 'objects':
            constructor=endpoint.return_class
            if not constructor:
                constructor=Generic
            exports=self.getall(result.json())
            objects=[]
            for item in exports:
                obj=constructor(item)
                objects.append(obj)
            return objects
        elif endpoint.return_type == 'text':
            return result.text
        else:
            return result

    def getall(self,json):
        for key, value in json.items():
            if key != 'pager':
                return value

    def get(self, path, **kwargs):
        return self.call(path, "GET", **kwargs)

    def put(self, path, **kwargs):
        return self.call(path, "PUT", **kwargs)

    def post(self, path, **kwargs):
        return self.call(path, "POST", **kwargs)

    def patch(self, path, **kwargs):
        return self.call(path, "PATCH", **kwargs)

    def delete(self, path, **kwargs):
        return self.call(path, "DELETE", **kwargs)

    def clear_hibernate_cache(self):
        return self._out(requests.get(self.baseurl + "/maintenance/cache"))


