import json
import httplib2
import urllib
import pprint


USER = "user"
CUSTOMER = "customer"
INVOICE = "invoice"
TRANSACTION = "transaction"
BILLING_PACKAGE = "billing_package"

def convert(input):
#http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-unicode-ones-from-json-in-python/6633651#6633651

    """ converts ascii to unicode for simplifying json output """

    if isinstance(input, dict):
        return {convert(key): convert(value) 
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class ChargeOverConnectionError(Exception):
    """ Connection errors thrown by ChargeOver """
    def __init__(self, code, text):
        self.value = str(code) + ": " + text
    def __str__(self):
        return repr(self.value)

class ChargeOverSyntaxError(Exception):
    """ Syntax (Bad URL, Bad options) errors thrown by ChargeOver """
    def __init__(self, code, text):
        self.value = str(code) + ": " + text
    def __str__(self):
        return repr(self.value)

class ChargeOver:

    """ For interacting with a ChargeOver server in python."""

    def __init__(self, endpoint, user, password, interactive=False):
        
        """ 
        endpoint, user and password should come from the
        "Configuration/API and webhooks" in your ChargeOver
        application when using Basic Authentication.

        Keyword Arguments: 
        interactive -- boolean, set to true if
        you're calling this in interactive mode.
        """
        
        self._endpoint = endpoint.rstrip("/")
        self._user = user
        self._pw = password
        self._interactive = interactive
        self._options = [USER, CUSTOMER, INVOICE, TRANSACTION, 
                         BILLING_PACKAGE]
        self._data = None
        self._http_res = None
        self._url = None

    def _prepare_connection(self):
        h = httplib2.Http()
        h.add_credentials(self._user, self._pw)
        self._response = None
        return h
    
    def _error_check(self):
        # HTTP response returned from httplib, this gives us HTTP
        # status information (also available in the json)
        if(self._http_res.status != 200 and 
           self._http_res.status != 302):
            raise ChargeOverConnectionError(self._http_res.status, 
                                            self._http_res.reason)

        # json response from ChargeOver server
        if(self._data['status'] != "OK"):
            raise ChargeOverSyntaxError(self._data['code'], 
                                        self._data['message'])
        return
      
    def _validate_target(self, target):
        if(self._interactive and target not in self._options):
            error = "Invalid target " + target + ". Use one of: "
            opts = ", ".join(self._options)
            raise Exception(error + opts)

    def _request(self, location, obj_id=None, where=None, limit=None, 
                 offset=None):
        self._validate_target(location)

        h = self._prepare_connection()

        opt_dict = {}

        if location:
            self._url = self._endpoint + "/" + location
        else:
            self._url = self._endpoint + "/"

        if obj_id is not None:
            self._url = self._url + "/" + str(obj_id)
        elif where is not None:
            # where and id are mutually exclusive
            where_str = None
            for key in where:
                if(where[key] == "NULL"):
                    clause = key + ":IS:NULL"
                else:
                    clause = key + ":EQUALS:" + str(where[key])
                if not where_str:
                    where_str = clause
                else:
                    where_str += "," + clause
            opt_dict['where'] = where_str
        
        if(limit):
            opt_dict['limit'] = str(limit)
        if(offset):
            opt_dict['offset'] = str(offset)

        if(opt_dict):
            suffix = None
            for key in opt_dict:
                if suffix:
                    suffix += "&" + key + "=" + opt_dict[key]
                else:
                    suffix = key + "=" + opt_dict[key]
            self._url += "?" + suffix

        http_res, content = h.request(self._url)

        # data is returned as a json object. This will convert it to
        # python structures in ascii. These are only saved for
        # debugging purposes.
        self._data = json.loads(content, object_hook=convert)
        self._http_res = http_res
        
        # the actual data. Calling method retrieves this.
        self._response = self._data['response']


    def _submit(self, location, data, obj_id=None):
        self._validate_target(location)

        http = self._prepare_connection()

        if location:
            self._url = self._endpoint + "/" + location
        else:
            self._url = self._endpoint + "/"

        method = "POST"
        if obj_id is not None:
            self._url = self._url + "/" + str(obj_id)
            method = "PUT"

        http_res, content = http.request(self._url, method, 
                                         json.dumps(data))

        self._data = json.loads(content, object_hook=convert)
        self._http_res = http_res

        self._response = self._data['response']


    def find_by_id(self, target, obj_id, pretty=False):
        """ retrieve an object from ChargeOver

        target -- string from the module data specifying what to
        retrieve, e.g. "customer", "invoice". These are constants in
        the module.

        Keyword Arguments:
        pretty -- set to True to get pretty printed output, surpresses
        return value. Only usable in interactive mode.

        return -- nothing when pretty is set to True in interactive
        mode. Otherwise, a dictionary or list of dictionaries
        containing the requested data."""

        self._request(target, obj_id)

        if(self._interactive and pretty):
            pprint.pprint(self._response)
            return

        if(self._http_res['status'] == '200'):
            return self._response
        elif(self._http_res['status'] == '404'):
            return None
        else:
            raise ChargeOverConnectionError(self._http_res.status, 
                                            self._http_res.reason)

    def find_all(self, target, limit=10, offset=None, pretty=False):
        """ retrieve an object from ChargeOver

        target -- string from the module data specifying what to
        retrieve, e.g. "customer", "invoice". These are constants in
        the module.

        Keyword Arguments:
        where -- dict for making more intelligent selections. Non null
        values will be turned into http GET options like
        key:EQUALS:value. 'value's set to "NULL" will be assigned as
        key:IS:NULL. see chargeover.com REST API documentation

        limit -- limits the number of results returned
        
        offset -- offset into results, useful for pagination

        pretty -- set to True to get pretty printed output, surpresses
        return value. Only usable in interactive mode.

        return -- nothing when pretty is set to True in interactive
        mode. Otherwise, a dictionary or list of dictionaries
        containing the requested data."""
        self._request(target, limit = locals()['limit'], 
                      offset = locals()['offset'])

        if(self._interactive and pretty):
            pprint.pprint(self._response)
            return

        if(self._http_res['status'] == '200'):
            return self._response
        else:
            raise ChargeOverConnectionError(self._http_res.status, 
                                            self._http_res.reason)

    def find(self, target, where, limit=10, offset=None, pretty=False):
        """ retrieve an object from ChargeOver

        target -- string from the module data specifying what to
        retrieve, e.g. "customer", "invoice". These are constants in
        the module.

        Keyword Arguments:
        where -- dict for making more intelligent selections. Non null
        values will be turned into http GET options like
        key:EQUALS:value. 'value's set to "NULL" will be assigned as
        key:IS:NULL. see chargeover.com REST API documentation

        limit -- limits the number of results returned

        offset -- offset into results, useful for pagination

        pretty -- set to True to get pretty printed output, surpresses
        return value. Only usable in interactive mode.

        return -- nothing when pretty is set to True in interactive
        mode. Otherwise, a dictionary or list of dictionaries
        containing the requested data."""
        self._request(target, where = locals()['where'],
                      limit = locals()['limit'], 
                      offset = locals()['offset'])

        if(self._interactive and pretty):
            pprint.pprint(self._response)
            return

        if(self._http_res['status'] == '200'):
            return self._response
        elif(self._http_res['status'] == '404'):
            return None
        else:
            raise ChargeOverConnectionError(self._http_res.status, 
                                            self._http_res.reason)

    def create(self, target, data, pretty=False):
        """ Add a new record to ChargeOver

        target -- string from class data (see get() for details)
        data -- object specific dictionary

        Keyword Arguments:
        pretty -- set to True to get pretty printed output, surpresses
        return value. Only usable in interactive mode.

        """
        if(self._interactive and target not in self._options):
            print "Invalid option " + target + ". Use one of:"
            for opt in options:
                print opt
            return

        self._submit(target, data)

        if(self._interactive and pretty):
            pprint.pprint(self._response)
            return

        if(self._http_res['status'] == '201'):
            return self._response
        elif(self._http_res['status'] == '404'):
            return None
        else:
            raise ChargeOverConnectionError(self._http_res.status, 
                                            self._http_res.reason)

    def update(self, target, obj_id, data, pretty=False):
        """ Update a ChargeOver record

        target -- string from class data (see get() for details)
        obj_id -- object id to modify
        data -- object specific dictionary
        
        pretty -- set to True to get pretty printed output, surpresses
        return value. Only usable in interactive mode.
        """

        if(self._interactive and target not in self._options):
            print "Invalid option " + target + ". Use one of:"
            for opt in options:
                print opt
            return

        self._submit(target, data, obj_id)

        if(self._interactive and pretty):
            pprint.pprint(self._response)
            return
 
        if(self._http_res['status'] == '202'):
            return self._response
        elif(self._http_res['status'] == '404'):
            return None
        else:
            raise ChargeOverConnectionError(self._http_res.status, 
                                            self._http_res.reason)


    def get_last_response(self):
        """ returns the response from ChargeOver as python objects """
        return self._data
        
    def get_last_http_response(self):
        """ returns the last http server response """
        return self._http_res
        
    def get_last_request_url(self):
        """ returns the last request url """
        return self._url
