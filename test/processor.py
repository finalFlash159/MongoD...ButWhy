import logging
import pandas as pd
import os
import re
import math
import numpy as np
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Chuyển tên cột tiếng Việt sang tên trường MongoDB (English snake_case)
FIELD_MAP = {
    'Ngày': 'ngay',
    'Nhà cung cấp': 'nha_cung_cap',
    'Hs code': 'hs_code',
    'Tên hàng': 'ten_hang',
    'Lượng': 'luong',
    'Đơn vị tính': 'don_vi_tinh',
    'Tên nước xuất xứ': 'xuat_xu',
    'Điều kiện giao hàng': 'dieu_kien_giao_hang',
    'Thuế suất XNK': 'thue_suat_xnk',
    'Thuế suất TTĐB': 'thue_suat_ttdb',
    'Thuế suất VAT': 'thue_suat_vat',
    'Thuế suất tự vệ': 'thue_suat_tu_ve',
    'Thuế suất BVMT': 'thue_suat_bvmt',
    'Trạng thái': 'tinh_trang',
    'file_name': 'file_name'
}


def xlsx_to_df(file_path: str) -> pd.DataFrame:
    logger.info(f"[xlsx_to_df] Đang đọc file Excel: {file_path}")
    df = pd.read_excel(file_path, engine='openpyxl')
    df = df.copy(deep=True)
    logger.info(f"[xlsx_to_df] Đọc xong file Excel, shape={df.shape}")
    return df


def remove_unwanted_chars(text: str) -> str:
    if not isinstance(text, str):
        return text
    while text.startswith("#&"):
        text = text[2:].lstrip()
    while text.endswith("#&"):
        text = text[:-2].rstrip()
    text = text.replace("'", "")
    text = text.replace("#&", ",")
    return text


def clean_special_chars_in_str_cols(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("[clean_special_chars_in_str_cols] Bắt đầu xử lý cột kiểu chuỗi.")
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):
            df.loc[:, col] = df[col].apply(remove_unwanted_chars)
    logger.info("[clean_special_chars_in_str_cols] Xong xử lý cột kiểu chuỗi.")
    return df


def process_supplier_name(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = re.sub(r"(?<!\., )\bLTD\b", r"., LTD", text)
    text = re.sub(r"\bLTD\b(?!\.)(?=\s|$)", r"LTD.", text)
    text = re.sub(r"\s*\.\s*", ".", text)
    text = re.sub(r"\s*,\s*", ",", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r",{2,}", ",", text)
    text = re.sub(
        r"([.,]+)",
        lambda m: ".," if '.' in m.group(0) and ',' in m.group(0) else m.group(0),
        text
    )
    return text


def process_supplier_column(df: pd.DataFrame) -> pd.DataFrame:
    if 'Nhà cung cấp' in df.columns:
        logger.info("[process_supplier_column] Bắt đầu xử lý cột 'Nhà cung cấp'.")
        df.loc[:, 'Nhà cung cấp'] = df['Nhà cung cấp'].astype(str).apply(process_supplier_name)
        logger.info("[process_supplier_column] Xong xử lý cột 'Nhà cung cấp'.")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("[remove_duplicates] Bắt đầu loại bỏ dòng trùng lặp.")
    before = len(df)
    df = df.drop_duplicates(keep='first')
    after = len(df)
    logger.info(f"[remove_duplicates] Đã loại bỏ {before - after} dòng trùng lặp. Còn {after} dòng.")
    return df.copy(deep=True)


def df_processor(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"[df_processor] Bắt đầu xử lý fillna, parse 'Ngày'. shape={df.shape}")
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df.loc[:, col] = df[col].fillna(value=np.nan)
        else:
            df.loc[:, col] = df[col].fillna("")
    if 'Ngày' in df.columns:
        df.loc[:, 'Ngày'] = pd.to_datetime(df['Ngày'], errors='coerce')
    tz_cols = df.select_dtypes(include=['datetimetz']).columns
    for col in tz_cols:
        df.loc[:, col] = df[col].dt.tz_localize(None)
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'Ngày':
            df.loc[:, col] = df[col].apply(
                lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, datetime.date)) and not pd.isnull(x) else x
            )
    df = clean_special_chars_in_str_cols(df)
    logger.info(f"[df_processor] Xong xử lý fillna, parse 'Ngày'. shape={df.shape}")
    return df


def create_file_name_column(df: pd.DataFrame, file_path: str) -> pd.DataFrame:
    logger.info("[create_file_name_column] Bắt đầu thêm cột 'file_name'.")
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    df.loc[:, 'file_name'] = base_name
    logger.info("[create_file_name_column] Đã thêm cột 'file_name'.")
    return df


def default_val(val, numeric: bool = False):
    if numeric:
        if isinstance(val, str):
            val = val.replace(',', '.')
        if pd.isna(val) or val == '' or val == 'NaN':
            return None
        else:
            return val
    else:
        if val is None or val == '' or (isinstance(val, float) and math.isnan(val)):
            return ''
        else:
            return val


def determine_status_column(df: pd.DataFrame) -> str:
    cols = [c.lower() for c in df.columns]
    if any('nhập' in c or 'nhap' in c for c in cols):
        return 'Nhập'
    elif any('xuất' in c or 'xuat' in c for c in cols):
        return 'Xuất'
    else:
        return ''


def store_dataframe_in_mongodb(df: pd.DataFrame,
                              mongo_uri: str,
                              db_name: str = 'project230255',
                              collection_name: str = 'hs_code') -> None:
    """
    Lưu DataFrame vào MongoDB với trường đã chuẩn hóa.
    """
    logger.info("[store_dataframe_in_mongodb] Kết nối MongoDB với URI: %s", mongo_uri)
    client = MongoClient(mongo_uri)
    db = client[db_name]
    coll = db[collection_name]

    # Chuyển DataFrame thành records và đổi tên cột
    df_renamed = df.rename(columns=FIELD_MAP)
    records = []
    for rec in df_renamed.to_dict(orient='records'):
        # Chuyển ngày thành ISO string
        if isinstance(rec.get('ngay'), (pd.Timestamp, datetime.date)):
            rec['ngay'] = rec['ngay'].isoformat()
        # Áp dụng default_val nếu cần
        rec = {k: default_val(v, k in ['luong','thue_suat_xnk','thue_suat_ttdb','thue_suat_vat','thue_suat_tu_ve','thue_suat_bvmt']) for k, v in rec.items()}
        records.append(rec)

    result = coll.insert_many(records)
    logger.info("[store_dataframe_in_mongodb] Đã insert %d documents.", len(result.inserted_ids))
    client.close()


def xlsx_processor_pipeline(file_path: str, mongo_uri: str, db_name: str = 'project230255'):
    logger.info(f"[xlsx_processor_pipeline] Bắt đầu, file_path={file_path}")
    df = xlsx_to_df(file_path)

    # Xác định và thêm cột Trạng thái
    status = determine_status_column(df)
    df['Trạng thái'] = status

    # Đổi tên cột gốc sang English keys
    # Lấy 13 cột đầu của file:
    if len(df.columns) < 13:
        raise ValueError("DataFrame có ít hơn 13 cột, không thể đổi tên.")
    

    # Tiếp tục xử lý
    df = df_processor(df)
    df = remove_duplicates(df)
    df = create_file_name_column(df, file_path)
    df = process_supplier_column(df)

    df.columns = list(FIELD_MAP.keys()) + list(df.columns[15:])
    # Lưu lên MongoDB
    store_dataframe_in_mongodb(df, mongo_uri, db_name=db_name)
    logger.info("[xlsx_processor_pipeline] Hoàn thành pipeline và lưu lên MongoDB.")


if __name__ == "__main__":
    load_dotenv()
    MONGODB_URI = os.environ.get('MONGODB_URI')
    FILE_PATH = "/Users/vominhthinh/Workspace/LogiTuning/data_upload_test/Nhập_01_0224.xlsx"
    xlsx_processor_pipeline(FILE_PATH, MONGODB_URI)
