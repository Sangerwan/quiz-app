import jwt
import datetime
from werkzeug.exceptions import Unauthorized


secret = "Super secret key know one will ever know, right ?"
expiration_in_seconds = 3600


class JwtError(Exception):
    """Exception raised for jwt errors in the quiz app 
    """

    def __init__(self, message="Jwt error"):
        self.message = message
        super().__init__(self.message)


def build_token(username):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_in_seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            secret,
            algorithm="HS256"
        )
    except Exception as e:
        return e


def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, secret, algorithms="HS256")
        # if decoding did not fail, this means we are correctly logged in
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise JwtError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError as e:
        raise JwtError('Invalid token. Please log in again.')

def encode_password(password):
    payload = {
        'password': password
    }
    encoded_password = jwt.encode(payload, secret, algorithm="HS256")
    return encoded_password

def check_password(password, encoded_password):
    try:
        payload = jwt.decode(encoded_password, secret, algorithms="HS256")
        if password == payload['password']:
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError as e:
        return False
