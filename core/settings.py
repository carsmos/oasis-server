import os
from typing import Optional, Dict
from pathlib import Path
from pydantic import BaseSettings

# 接口限流次数
TIMES = 30

# 数据库连接配置
MYSQL_PASSWD = os.environ.get('MYSQL_ROOT_PASS')
MYSQL_PORT = os.environ.get('MYSQL_PORT')
DATABASE_MASTER_URI = 'mysql://root:{}@{}:3306/oasis'.format(MYSQL_PASSWD, os.environ.get('MYSQL_HOST'))
# DATABASE_SLAVE_URI = os.environ.get('DATABASE_SLAVE_URI')

# 数据库配置
TORTOISE_ORM: Dict = {
    'connections': {
        'default': DATABASE_MASTER_URI,
        # 'slave': DATABASE_SLAVE_URI
    },
    'apps': {
        'models': {
            # 设置key值“default”的数据库连接
            'default_connection': 'default',
            'models': [
                'apps.user.model', "aerich.models", 'apps.car.model', 'apps.dynamic.model',
                'apps.job.model', 'apps.light.model', 'apps.scenario.model', 'apps.sensor.model',
                'apps.task.model', 'apps.weather.model', 'apps.traffic_flow.model', 'apps.log.model',
                'apps.evaluation_criteria.model', 'casbin_tortoise_adapter', 'apps.controller.model'
            ]
        }
    },
    "routers": ["database.Router"],
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


class APISettings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = os.environ.get('DEBUG', True)

    # 项目文档
    TITLE: str = "oasis server"

    DESCRIPTION: str = "基于mysql"

    # 项目根路径
    BASE_PATH: Path = Path(__file__).resolve().parent.parent

    # 文档地址 默认为docs
    DOCS_URL: str = os.path.join(BASE_PATH, 'docs')
    ACCESS_TOKEN_EXPIRE_MINUTES = 8 * 60

    # 权限控制配置
    CASBIN_MODEL_PATH: Path = BASE_PATH.joinpath('config/rbac_model.conf')

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # SECRET_KEY
    SECRET_KEY: str = "safewfcxoofaewfppgjkaiajljg8aojgegkkja@jgsai"

    # 不需要登录认证的 API
    NO_VERIFY_URL: Dict = {
        "/": "eq",  # 根目录
        '/auth/jwt/login': "in",
        '/emails/send_email_logout': 'in',
        "/upload/upload_files": 'in'
    }

settings = APISettings()