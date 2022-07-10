from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


def generate_hash(password):
    return pwd_context.hash(password)


def verify_hash(password, hash):
    return pwd_context.verify(password, hash)
