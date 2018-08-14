import hashlib


def pwd_encrypted(get_pwd):
    salt = 'cqgynet'
    hash_key = hashlib.sha256()
    hash_key.update((str(get_pwd) + salt).encode('utf8'))
    pwd = hash_key.hexdigest()
    return pwd
