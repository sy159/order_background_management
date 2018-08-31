import hashlib, random, string


def pwd_encrypted(get_pwd):
    '''管理员加密方法'''
    salt = 'cqgynet'
    hash_key = hashlib.sha256()
    hash_key.update((str(get_pwd) + salt).encode('utf-8'))
    pwd = hash_key.hexdigest()
    return pwd


def pwd(password):
    '''
    配送员加密方法
    '''
    password = str(password)
    hash_value = hashlib.sha256()
    hash_key = hashlib.sha256()
    hash_key.update(password.encode())
    password = hash_key.hexdigest()  # 先把密码sha256加密
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    hash_value.update((password + salt).encode())
    return hash_value.hexdigest() + salt
