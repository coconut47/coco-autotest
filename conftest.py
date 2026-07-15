from common.config import SERVER_URL
import pytest
import time
import requests

from utils.data_utils import clear_extract_yaml, extract_yaml, read_yaml
from utils.rsa_utils import PasswordEncryptor
import logging


# 配置日志记录器
logger = logging.getLogger("TestWork")

@pytest.fixture(scope='session',autouse=False)
def get_admin_token():

    username = 'admin'
    password = "123456"
    user_type = "admin"

    # 从 extract.yaml 读取自动获取的公钥
    public_key = read_yaml("config/extract.yaml")["publicKey"]
    entrytor = PasswordEncryptor()
    pem_public_key = "-----BEGIN PUBLIC KEY-----" + public_key + "-----END PUBLIC KEY-----"
    entrytor.set_public_key(pem_public_key)
    password_rsa = entrytor.encryptPassword(password)

    params = {
        "username": username,
        "password": password_rsa,
        "userType": user_type,
        "timestamp": int(time.time() * 1000)
    }

    session = requests.Session()
    resp = session.request("POST", SERVER_URL+"/login", json=params)
    resp.raise_for_status()
    token = resp.json()["data"]["token"]
    session.headers.update({
        "Token": token
    })
    extract_yaml("init_token", token)

    yield session

    session.close()

@pytest.fixture(scope='session',autouse=False)
def get_user_token():

    username = 'ZZULI123456'
    password = "123456"
    user_type = "user"

    # 从 extract.yaml 读取自动获取的公钥
    public_key = read_yaml("config/extract.yaml")["publicKey"]
    entrytor = PasswordEncryptor()
    pem_public_key = "-----BEGIN PUBLIC KEY-----" + public_key + "-----END PUBLIC KEY-----"
    entrytor.set_public_key(pem_public_key)
    password_rsa = entrytor.encryptPassword(password)

    params = {
        "username": username,
        "password": password_rsa,
        "userType": user_type,
        "timestamp": int(time.time() * 1000)
    }

    session = requests.Session()
    resp = session.request("POST", SERVER_URL+"/login", json=params)
    resp.raise_for_status()
    token = resp.json()["data"]["token"]
    session.headers.update({
        "Token": token
    })
    extract_yaml("init_token", token)

    yield session

    session.close()




@pytest.fixture(scope='session',autouse=True)
def setup_and_teardown():

    logger = logging.getLogger("TestWork")
    logger.info("初始化配置中...测试会话即将开始...")

    clear_extract_yaml()

    # 自动从后端获取RSA公钥
    try:
        resp = requests.get(SERVER_URL + "/login/auth/publicKey")
        resp.raise_for_status()
        public_key = resp.json()["data"]["publicKey"]
        extract_yaml("publicKey", public_key)
        logger.info("公钥获取成功")
    except Exception as e:
        logger.error(f"公钥获取失败: {e}")
        raise

    logger.info("初始化配置完成,测试会话开始!")
    yield
    logger.info("测试会话结束...关闭测试环境...")






