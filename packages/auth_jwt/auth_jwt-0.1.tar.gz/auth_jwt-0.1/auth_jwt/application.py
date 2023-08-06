import jwt
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request


def verify_jwt(token, secret):
    """Verify if token is valid."""
    options = {
        'verify_signature': True,
        'verify_exp': True
    }

    decoded_token = jwt.decode(token, secret, options=options)

    return decoded_token


def create_jwt(client_id, secret):
    """Create a new token."""
    token = jwt.encode(
        {
            'client': client_id,
            'exp': datetime.utcnow() + timedelta(seconds=10)
        },
        secret,
        algorithm='HS256'
    )

    return token


def verify_client_request(func):
    """Decorator must be aplied to Flask handler."""
    def inner(*args):
        """Decorator to verify client request."""

        self = args[0]
        if self:
            if issubclass(self.__class__, Resource):
                if 'Inbound-Appid' in request.headers:
                    print request.headers.get('Inbound-Appid')
                else:
                    pass

                print dir(self)

        return func(*args)
    return inner


def main():
    # print create_jwt('client', 'secret')
    print verify_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnQiOiJjbGllbnQiLCJleHAiOjE0NTkyODc2ODV9.lrmZpgxhp7mBcHTQDqG_41VfLdeK9Kx3uCAKXnXgkkY', 'secret')


if __name__ == '__main__':
    main()
