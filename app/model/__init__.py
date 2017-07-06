from pymongo import MongoClient
import ssl

db_url = '########################$$$$$$$$$$$$$$$$$$$$$$$$'   ##替换
client = MongoClient(db_url,ssl_cert_reqs = ssl.CERT_NONE)
db = client['testDB']
#db = client['testDB1']
