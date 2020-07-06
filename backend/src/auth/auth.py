import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsndmh.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'HTTP://127.0.0.1:8080'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header
def get_token_auth_header():
    '''return Token from the Authorization Header'''
    # attempting to get the header from the request
    auth = request.headers.get('Authorization', None)
    # raising an AuthError if no header is present
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    # spliting bearer and the tokensplit bearer and the token
    parts = auth.split()
    # raising an AuthError if the header is malformed
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    # raising an AuthError if the header is malformed
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    # raising an AuthError if the header is malformed
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    # return the token part of the header
    return token


def check_permissions(permission, payload):
    '''obtain true if the requested permission in the payload permissions'''
    # raiseing an AuthError becuase permissions are not included in the payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    # raiseing an AuthError becuase the requested permission string is not in
    # the payload permissions
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    # otherwise return true
    return True


def verify_decode_jwt(token):
    '''takeing the encoded token as parameters and validating it after decoded'''
    # get public key from Auth0
    myurl = 'https://%s/.well-known/jwks.json' % (AUTH0_DOMAIN)
    jsonurl = urlopen(myurl)
    content = jsonurl.read().decode(jsonurl.headers.get_content_charset())
    jwks = json.loads(content)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    # check if Auth0 token with key id
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # validate the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # return the decoded payload
            return payload
        # catch some errors
        except jwt.ExpiredSignatureError:
            # raise AuthError if token expired
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            # raise AuthError if we have invalid claims
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    '''Decorator method  for make authorization to endpoints'''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get the token
            token = get_token_auth_header()
            # decode the jwt and get payload
            payload = verify_decode_jwt(token)
            # validate claims and check the requested permission
            check_permissions(permission, payload)
            # return decorator with passing  decoded payload
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
