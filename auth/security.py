from passlib.hash import bcrypt

def hash_pwd(pwdPlain:str):
    return bcrypt.hash(pwdPlain)

def check_pwd(pwdPlain:str,pwdHash:str):
    return True if bcrypt.verify(hash=pwdHash,secret=pwdPlain) else False 