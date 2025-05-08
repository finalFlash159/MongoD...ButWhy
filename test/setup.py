from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# 1. Kết nối

client = MongoClient(MONGODB_URI)

# 2. Lấy reference (nếu chưa tồn tại, driver sẽ tạo khi insert)
db = client["project230255"]
coll = db["hs_code"]

# 2. Pipeline fuzzy tìm cả tên hàng, nhà cung cấp, mã HS

threshold = 0.0
pipeline=[
  {
    "$match": {
      "hs_code": {
        "$regex": "0105",
        "$options": "i"
      }
    }
  },
  {
    "$limit": 20
  }
]

results = list(coll.aggregate(pipeline))
for doc in results:
    print(doc)