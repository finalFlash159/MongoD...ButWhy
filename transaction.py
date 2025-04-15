import os
import pprint
from dotenv import load_dotenv
from pymongo import MongoClient

# Load config từ file .env
load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

# Kết nối tới MongoDB cluster
client = MongoClient(MONGODB_URI)

# Hàm callback định nghĩa logic của transaction
def callback(
    session,
    transfer_id=None,
    account_id_receiver=None,
    account_id_sender=None,
    transfer_amount=None,
):
    # Tham chiếu đến collection accounts và transfers
    accounts_collection = session.client.bank.accounts
    transfers_collection = session.client.bank.transfers

    # Tạo tài liệu ghi lại thông tin chuyển tiền
    transfer = {
        "transfer_id": transfer_id,
        "to_account": account_id_receiver,
        "from_account": account_id_sender,
        "amount": {"$numberDecimal": transfer_amount},
    }

    # Cập nhật tài khoản người gửi: trừ tiền và lưu lịch sử giao dịch
    accounts_collection.update_one(
        {"account_id": account_id_sender},
        {
            "$inc": {"balance": -transfer_amount},
            "$push": {"transfers_complete": transfer_id},
        },
        session=session,
    )

    # Cập nhật tài khoản người nhận: cộng tiền và lưu lịch sử giao dịch
    accounts_collection.update_one(
        {"account_id": account_id_receiver},
        {
            "$inc": {"balance": transfer_amount},
            "$push": {"transfers_complete": transfer_id},
        },
        session=session,
    )

    # Thêm bản ghi chuyển khoản vào collection transfers
    transfers_collection.insert_one(transfer, session=session)

    print("Transaction successful")

# ✅ Wrapper cho callback để truyền session và các tham số
def callback_wrapper(s):
    callback(
        s,
        transfer_id="TR218721873",
        account_id_receiver="MDB343652528",
        account_id_sender="MDB574189300",
        transfer_amount=100,
    )

# Khởi động phiên làm việc và chạy transaction
with client.start_session() as session:
    session.with_transaction(callback_wrapper)

# Đóng kết nối sau khi xong
client.close()