# this file is responsible for signing, encoding, decogind and return JWTs

# set expiration limit for the tokens
import time
import datetime
# resposible for encondig and decogind generated token
import jwt
import re

# organize settings
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
NUM_SECONDS_IN_A_MIN = 60

#User can be logged in for 20 minutes
ACCESS_TOKEN_EXPIRE_SECONDS = 1200


# function returns generated token
def token_reponse(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str, userOffice: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS,
        "userOffice": userOffice
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_reponse(token)


def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
    except Exception as e:
        return {'error': str(e)}


def verify_user_office_can_access_endpoint(office, request_method, request_route):
    request_route = re.sub(r'[0-9]+', '', request_route)
    ADMIN_ROUTES = ['/authors/', '/papers/']
    ADMIN_METHODS = ['POST', 'PATH', 'DELETE']

    if request_method in ADMIN_METHODS and request_route in ADMIN_ROUTES:
        return True if office == 'Admin' else False
    return True


def verify_token(token: str, request_method, request_route):
    try:
        decode_token = decode_jwt(token)
        if decode_token:
            office = decode_token['userOffice']
            user_access = verify_user_office_can_access_endpoint(office, request_method, request_route)
            if not user_access:
                return {}
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}


def verify_minutes(minutes):
    return 's' if minutes > 1 else ''


def personalize_message(life_time_in_minutes, is_minute_singular_or_plural):
    message = 'Your token will expiry in less than 1 minute.' if life_time_in_minutes < 0 \
              else f'Your token will expire in {life_time_in_minutes} minute{is_minute_singular_or_plural}.'

    return {'message': message}


def get_expiry_token(request):
    get_jwt_from_request = request.headers.raw[3][1].decode('utf-8').split(' ')[1]

    try:
        decoded_token = decode_jwt(get_jwt_from_request)
    except Exception as e:
        return {'error': str(e)}

    time_to_end_session = datetime.datetime.fromtimestamp(decoded_token['expiry'])
    now = datetime.datetime.now()
    life_time_in_minutes = int(((time_to_end_session - now).total_seconds()) / NUM_SECONDS_IN_A_MIN)

    is_minute_singular_or_plural = verify_minutes(life_time_in_minutes)

    return personalize_message(life_time_in_minutes, is_minute_singular_or_plural)
