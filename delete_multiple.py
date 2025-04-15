import os
import pprint
from dotenv import load_dotenv
from pymongo import MongoClient

# Load config từ file .env
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# Kết nối tới MongoDB cluster
client = MongoClient(MONGODB_URI)

# Truy cập database 'bank'
db = client.bank

# Truy cập collection 'accounts'
accounts_collection = db.accounts

# Lọc các document có balance < 2000
documents_to_delete = {"balance": {"$lt": 2000}}

# In ra một document mẫu trước khi xóa
print("🔍 Searching for sample target document before delete:")
pprint.pprint(accounts_collection.find_one(documents_to_delete))

# Xóa các document thỏa điều kiện
result = accounts_collection.delete_many(documents_to_delete)

# In ra một document mẫu sau khi xóa
print("🔍 Searching for sample target document after delete:")
pprint.pprint(accounts_collection.find_one(documents_to_delete))

# In số lượng document đã bị xóa
print("🗑️ Documents deleted: " + str(result.deleted_count))

# Đóng kết nối
client.close()