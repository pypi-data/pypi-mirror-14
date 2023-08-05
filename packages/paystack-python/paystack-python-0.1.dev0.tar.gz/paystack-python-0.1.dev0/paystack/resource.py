import paystack, json
from paystack.http_client import RequestsClient

def populate_headers(secret_key):
    if secret_key is not None:
        return {"Authorization": secret_key, "Content-Type": "application/json"}

def parse_response(response):
    resp = json.loads(response.content)
    resp = resp.get('data')
    return resp


def convert_to_paystack_object(resp, klass_name = None):
    types = {
        'customer': Customer,
        'transaction': Transaction,
        'plan': Plan
    }
    if isinstance(resp, dict):
        resp = resp.copy()
        if isinstance(klass_name, basestring) and not isinstance(resp, Paystack):
            klass = types.get(klass_name, Paystack)
        else:
            klass = Paystack
        return klass.construct_from(resp)
    else:
        return resp

class Paystack(dict):

    def __init__(self, id = None, **params):
        super(Paystack, self).__init__()
        self._unsaved_values = set()
        if id:
            self['id'] = id

    def __getitem__(self, k):
        return super(Paystack, self).__getitem__(k)

    def __setitem__(self, k, v):
        super(Paystack, self).__setitem__(k, v)
        self._unsaved_values.add(k)

    def __getattr__(self, k):
            return self[k]

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(Paystack, self).__setattr__(k, v)
        else:
            self[k] = v

    def __str__(self):
        return json.dumps(self, sort_keys = True, indent = 3)

    def serialize(self):
        params = {}
        unsaved_keys = self._unsaved_values or set()

        for k, v in self.items():
            if k == 'id' or (isinstance(k, str) and k.startswith('_')):
                continue
            elif k in unsaved_keys:
                params[k] = v
        return params

    @classmethod
    def construct_from(cls, values):
        instance = cls(values.get('id'))
        instance.refresh_from(values)
        return instance

    def refresh_from(self, values):
        for k, v in values.iteritems():
            super(Paystack, self).__setitem__(
                k,v)

class APIResource(Paystack):

    @classmethod
    def retrieve(cls, id):
        instance = cls(id)
        instance.refresh()
        return instance

    @classmethod
    def class_url(cls):
        cls_url = paystack.api_url + '/' + cls.class_name() + '/'
        return cls_url

    @classmethod
    def class_name(cls):
        cls_name = cls.__name__.lower()
        return cls_name

    def instance_url(self):
        id = self.get('id')
        return self.class_url() + str(id)

    def refresh(self):
        response = RequestsClient().request('get', self.instance_url(), self.fill_headers())
        self.refresh_from(parse_response(response))
        return self

    @classmethod
    def fill_headers(cls):
        paystack_headers = populate_headers(paystack.secret_key)
        return paystack_headers


class ListableAPIResource(APIResource):
    @classmethod
    def list(cls):
        url = cls.class_url()
        response = RequestsClient().request('get', url, cls.fill_headers())
        return response.content


class CreateableAPIResource(APIResource):
    @classmethod
    def create(cls, **params):
        url = cls.class_url()
        response= RequestsClient().request('post', url, cls.fill_headers(), json.dumps(params))
        return convert_to_paystack_object(parse_response(response), cls.class_name())

class UpdateableAPIResource(APIResource):
    def save(self):
        updated_params = self.serialize()
        response = RequestsClient().request('put', self.instance_url(),
                                           self.fill_headers(), json.dumps(updated_params))
        if updated_params:
            self.refresh_from(parse_response(response))
        return self

class Customer(CreateableAPIResource,
               UpdateableAPIResource,
               ListableAPIResource):
    pass

class Transaction(CreateableAPIResource,UpdateableAPIResource,ListableAPIResource):
    @classmethod
    def initialize(cls, **params):
       url = cls.class_url() + 'initialize'
       response = RequestsClient().request('post', url, cls.fill_headers(), json.dumps(params))
       return convert_to_paystack_object(parse_response(response), cls.class_name())

    @classmethod
    def charge_token(cls, **params):
        url = cls.class_url() + 'charge_token'
        response = RequestsClient().request('post', url, cls.fill_headers(), json.dumps(params))
        return convert_to_paystack_object(parse_response(response), cls.class_name())

    @classmethod
    def charge_authorization(cls, **params):
        url = cls.class_url() + 'charge_authorization'
        response = RequestsClient().request('post', url, cls.fill_headers(), json.dumps(params))
        return convert_to_paystack_object(parse_response(response), cls.class_name())

    @classmethod
    def verify(cls, reference):
       url = cls.class_url() + 'verify/' + str(reference)
       response = RequestsClient().request('get', url, cls.fill_headers())
       return convert_to_paystack_object(parse_response(response), cls.class_name())

    @classmethod
    def totals(cls):
       url = cls.class_url() + 'totals/'
       response = RequestsClient().request('get', url, cls.fill_headers())
       return convert_to_paystack_object(parse_response(response), cls.class_name())

class Plan(CreateableAPIResource,
           UpdateableAPIResource,
           ListableAPIResource):
    pass