import walrus
from sdgApp.Infrastructure.conf_parser import get_conf


def redis_session() -> walrus.Database:
    conf = get_conf()
    host = str(conf['DB_REDIS']['REDIS_HOST'])
    port = int(conf['DB_REDIS']['REDIS_PORT'])
    db = int(conf['DB_REDIS']['REDIS_DB'])
    password = str(conf['DB_REDIS']['REDIS_PASSWORD'])
    session = walrus.Database(host=host,
                              port=port,
                              db=db,
                              decode_responses=True,
                              password=password)
    session.ping()
    return session


async def get_redis():
    try:
        sess = redis_session()
        yield sess
    finally:
        sess.close()
