# this file is responsible for signing, encoding, decogind and return JWTs

# set expiration limit for the tokens
import time

# resposible for encondig and decogind generated token
import jwt

# organize settings
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# function returns generated token
def token_reponse(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_reponse(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}
