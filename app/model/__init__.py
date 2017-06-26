from pymongo import MongoClient
import ssl

db_url = 'mongodb://admin:MHFUHVSQTMAMKENR@bluemix-sandbox-dal-9-portal.8.dblayer.com:27271,bluemix-sandbox-dal-9-portal.6.dblayer.com:27271/admin?ssl=true'
client = MongoClient(db_url,ssl_cert_reqs = ssl.CERT_NONE)
db = client['testDB']
#db = client['testDB1']
