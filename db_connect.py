from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ye:1111@cluster0.zcgo2.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client['graduation_work']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)