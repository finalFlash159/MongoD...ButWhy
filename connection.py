from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://myAtlasDBUser:thinh4526@myatlasclusteredu.7ezulr9.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"

client = MongoClient(MONGODB_URI)

# test connection
for db in client.list_database_names():
    print(db)