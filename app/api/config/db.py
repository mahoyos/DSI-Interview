#from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importing MYSQL configs from the configuration module
from app.api.config.env import  DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class MySQLDB:
    def __init__(self, host: str, user: str, password: str, db_name: str):
        SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
        self._engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @property
    def engine(self):
        return self._engine

mysql_db = MySQLDB(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)


'''
The connection to Mongo is disabled since the credentials from the
.env.example were not working, which caused errors. It can be uncommented 
when appropriate values are added to the .env.


# Importing MONGO_CLIENT from the configuration module
from app.api.config.env import MONGO_CLIENT, DB_NAME_MONGO

class Database:
    def __init__(self, uri: str):
        self._client = MongoClient(uri)
        self._db = self._client[DB_NAME_MONGO]

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db
    
    # Collections
    @property
    def items(self):
        return self._db.items
    
database = Database(MONGO_CLIENT)
'''