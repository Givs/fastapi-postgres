# this file is responsible for signing, encoding, decogind and return JWTs

# set expiration limit for the tokens
import time
from fastapi import FastAPI, status, HTTPException, Body, Depends

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


def signJWT(userID: str, userOffice: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600,
        "userOffice": userOffice
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_reponse(token)


def decodeJWT(token: str, request_method, request_route):
    #TODO tirar essa verificação de rotas admin daqui
    admin_routes = ['/authors', '/papers']
    admin_methods = ['POST', 'PATH']
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        if decode_token:
            office = decode_token['userOffice']
            if request_method in admin_methods and request_route in admin_routes:
                if office != 'Admin':
                    return {}
            return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}
