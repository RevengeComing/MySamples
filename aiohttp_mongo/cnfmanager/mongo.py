import motor.motor_asyncio

def create_mongodb_client(port, host, db):

    connection_uri = 'mongodb://{host}:{port}'.format(
        host=host, port=port
    )
    client = motor.motor_asyncio.AsyncIOMotorClient()
    return client

async def init_mongodb(app):
    """
    This function runs to initilize mongodb database.
    """
    conf = app['config']['mongodb']
    port = conf.get('port',27017)
    host = conf.get('host', 'localhost')
    db = conf.get('database', 'test')

    # user = conf.get('user', None)
    # password = conf.get('password', None)
    
    client = create_mongodb_client(port, host, db)
    app['db'] = client[db]

async def close_mongodb(app):
    """
    This function runs whenever application is going to be closed.
    """
    pass