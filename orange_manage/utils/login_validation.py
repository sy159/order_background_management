import pyotp


def validation(secret_key, verifycode):
    t = pyotp.TOTP(secret_key)
    result = t.verify(verifycode)  # 对输入验证码进行校验，正确返回True
    judge = result if result is True else False
    return judge
