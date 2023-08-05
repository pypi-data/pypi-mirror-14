secret_key = None
api_url = 'https://api.paystack.co'
headers = None

from paystack.resource import Transaction, Customer, Plan
from paystack.error import ApiConnectionError, AuthenticationError, InternalServerError, InvalidRequestError