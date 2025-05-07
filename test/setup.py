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
pipeline = [
  # 1) Search với fuzzy
  {
    "$search": {
      "compound": {
        "should": [
          {
            "text": {
              "query": "chim bồ câu",
              "path": "Tên hàng",
              "fuzzy": {
                "maxEdits": 1,               # chỉ 1 ký tự sai
                "prefixLength": 1,           # 2 ký tự đầu phải khớp
                "maxExpansions": 20          # tối đa 20 biến thể
              }
            }
          }
        ]
      }
    }
  },
  # 2) Thêm trường score mà vẫn giữ nguyên tất cả các trường khác
  {
    "$set": {
      "score": { "$meta": "searchScore" }
    }
  },
  # 3) Lọc theo threshold
  {
    "$match": {
      "score": { "$gte": threshold }
    }
  },
  # 4) Giới hạn kết quả
  {
    "$limit": 20
  }
]

results = list(coll.aggregate(pipeline))
for doc in results:
    print(doc)