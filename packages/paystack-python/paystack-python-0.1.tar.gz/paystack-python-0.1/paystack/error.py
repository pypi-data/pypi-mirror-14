import sys

class PaystackError(Exception):
   def __init__(self, message = None, http_status = None):
       super(PaystackError, self).__init__(message)

       self.message = message
       self.http_status = http_status


class ApiConnectionError(PaystackError):
    pass

class AuthenticationError(PaystackError):
    pass

class InvalidRequestError(PaystackError):
    pass

class InternalServerError(PaystackError):
    pass
