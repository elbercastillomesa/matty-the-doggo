from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb://mongo-db:27017'

ca = certifi.where()


def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["mongo-db"]
    except ConnectionError:
        print('Database Connection Error')
    return db