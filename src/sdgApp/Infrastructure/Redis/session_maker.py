import walrus
from sdgApp.Infrastructure.conf_parser import get_conf

def redis_session() -> walrus.Database:
    conf = get_conf()
    host = str(conf['Queue Redis']['host'])
    port = int(conf['Queue Redis']['port'])
    db = int(conf['Queue Redis']['db'])
    password = str(conf['Queue Redis']['password'])
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