import error, json

try:
    import requests
except ImportError:
    requests = None

class HTTPClient(object):
    def __init__ (self):
        pass

    def request(self, method, url, headers, data= None):
        pass

class RequestsClient(HTTPClient):
    def request(self, method, url, headers, data = None):
        try:
            response = requests.request(method, url, headers = headers, data = data)
            if response.status_code in [400, 401, 404, 500]:
                return handle_errors(response.status_code, response)
            return requests.request(method, url, headers = headers, data = data)
        except TypeError as e:
            return e

def handle_errors(status_code, response):
    resp = json.loads(response.content)
    if status_code == 500:
        raise error.InternalServerError(resp.get('message'), response.status_code)
    elif status_code == 401:
        raise error.AuthenticationError(resp.get('message'), response.status_code)
    elif status_code in [400, 404]:
        raise error.InvalidRequestError(resp.get('message'), response.status_code)