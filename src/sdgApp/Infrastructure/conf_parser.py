import os
import configparser


def get_conf():
    CONFIG_FILE_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../..', 'conf.ini'))
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    # need to update if there new params
    if os.environ.get("REDIS_HOST") is not None:
        config['DB_REDIS']['REDIS_HOST'] = os.environ.get("REDIS_HOST")
    if os.environ.get("REDIS_PORT") is not None:
        config['DB_REDIS']['REDIS_PORT'] = os.environ.get("REDIS_PORT")
    if os.environ.get("REDIS_DB") is not None:
        config['DB_REDIS']['REDIS_DB'] = os.environ.get("REDIS_DB")
    if os.environ.get("REDIS_PASSWORD") is not None:
        config['DB_REDIS']['REDIS_PASSWORD'] = os.environ.get("REDIS_PASSWORD")
    if os.environ.get("USER_ID") is not None:
        config['DB_REDIS']['USER_ID'] = os.environ.get("USER_ID")

    if os.environ.get("MONGO_CONNECTION_STRING") is not None:
        config['DB_MONGO']['MONGO_CONNECTION_STRING'] = os.environ.get(
            "MONGO_CONNECTION_STRING")
    if os.environ.get("MONGO_DB_NAME") is not None:
        config['DB_MONGO']['MONGO_DB_NAME'] = os.environ.get("MONGO_DB_NAME")
    return config
