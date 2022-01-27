import os
import configparser


def get_conf():
    CONFIG_FILE_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../..', 'conf.ini'))
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    # need to update if there new params
    if os.environ.get("redis_host") is not None:
        config['Queue Redis']['host'] = os.environ.get("redis_host")
    if os.environ.get("redis_port") is not None:
        config['Queue Redis']['port'] = os.environ.get("redis_port")
    if os.environ.get("redis_db") is not None:
        config['Queue Redis']['db'] = os.environ.get("redis_db")
    if os.environ.get("redis_password") is not None:
        config['Queue Redis']['password'] = os.environ.get("redis_password")

    if os.environ.get("mongo_connection_string") is not None:
        config['DB Mongo']['connection_string'] = os.environ.get(
            "mongo_connection_string")
    if os.environ.get("mongo_db_name") is not None:
        config['DB Mongo']['db_name'] = os.environ.get("mongo_db_name")
    return config
