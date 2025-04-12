from pymongo import MongoClient

# replace <password> with your actual password
MONGODB_URI = "mongodb+srv://myAtlasDBUser:<password>@myatlasclusteredu.7ezulr9.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"

client = MongoClient(MONGODB_URI)

# test connection
for db in client.list_database_names():
    print(db)