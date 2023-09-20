from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.uri_parser import parse_uri
import urllib.parse


username = 'adddmin'
passw = 'vhgTfv8xom24Kkn4'

username = urllib.parse.quote_plus(username)
passw = urllib.parse.quote_plus(passw)

uri = f"mongodb+srv://{username}:{passw}@cluster0.wvqfpmi.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)