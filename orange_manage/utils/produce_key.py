import pyotp


def login_key():
    gtoken = pyotp.random_base32()
    return gtoken
