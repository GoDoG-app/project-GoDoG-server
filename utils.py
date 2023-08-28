from passlib.hash import pbkdf2_sha256
from config import Config


# 1. 원문 비밀번호를, 단방향으로 암호화 하는 함수.
def hash_password(original_password) :
    password =  pbkdf2_sha256.hash(original_password + Config.SALT)
    return password


# 2. 유저가 입력한 비밀번호가, 맞는지 체크하는 함수
def check_password(original_password, hashed_password) :
    check = pbkdf2_sha256.verify(original_password + Config.SALT, hashed_password)
    return check # True, False 로 나옴.