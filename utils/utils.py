import base64
import math
import re
import threading
import uuid

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from passlib.context import CryptContext

from core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Singleton(type):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        with cls._instance_lock:
            if not hasattr(cls, '_instance'):
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def gen_uuid() -> str:
    # 生成uuid
    # https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy?rq=1
    return uuid.uuid4().hex


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password: 原密码
    :param hashed_password: hash后的密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    获取 hash 后的密码
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def validate_email_and_pw(usename, password):
    reason_list = []
    if len(usename) > 32:
        reason_list.append("用户名须小于32位")
    if len(usename) < 3:
        reason_list.append("用户名须大于3位")
    if not re.findall("^[0-9a-zA-Z._!@#$%^&*+-]+$", usename):
        reason_list.append("用户名必须满足注册规则")
    # if len(email) > 32:
    #     reason_list.append("email长度须小于32位")
    # if len(email) < 7:
    #     reason_list.append("email长度须大于7位")
    # if re.findall("[\u4e00-\u9fa5]", email):
    #     reason_list.append("email不能存在中文")
    # if not re.match(r'^[0-9A-Za-z!#$%^&*()_+?-]+@[0-9A-Za-z_]+\.(com|cn)$', email):
    #     reason_list.append("email格式错误")
    if len(password) > 32:
        reason_list.append("密码长度须小于32位")
    if len(password) < 6:
        reason_list.append("密码长度须大于6位")
    if not re.match(r'[0-9A-Za-z!@#$%^&*()_+?;:-]', password):
        reason_list.append("密码格式校验失败")
    if len(reason_list) > 0:
        return False, reason_list
    else:
        return True, None


def paginate(count, pagesize):
    if count <= 0:
        return {'total_num': 0, 'total_page_num': 0}
    if pagesize == 0:
        return {'total_num': count, 'total_page_num': 1}
    total_num = count
    total_page = math.ceil(total_num / pagesize)
    return {'total_num': total_num, 'total_page_num': total_page}

def rsa_decode(cipher_text):
    rsakey = RSA.importKey(settings.RSA_PRIVATE_KEY)  # 导入读取到的私钥
    cipher = PKCS1_v1_5.new(rsakey)  # 生成对象
    # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
    text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
    return text.decode()