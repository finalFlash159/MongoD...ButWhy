import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize the LLM
template_system = (
    "Bạn là chuyên gia MongoDB search và query. "
    "User có thể hỏi bất kỳ trường nào trong bộ dữ liệu sau:"
    "['ngay','nha_cung_cap','hs_code','ten_hang','luong','don_vi_tinh',"
    "'xuat_xu','dieu_kien_giao_hang','thue_suat_xnk','thue_suat_ttdb',"
    "'thue_suat_vat','thue_suat_tu_ve','thue_suat_bvmt']" 
    "Phân tích câu hỏi và phân loại truy vấn vào các nhóm sau:"
    "1. FUZZY_SEARCH: Chỉ áp dụng cho trường 'ten_hang' và 'nha_cung_cap'"
    "2. REGEX: Chỉ áp dụng cho trường 'hs_code'"
    "3. EXACT_MATCH: Áp dụng cho tất cả các trường còn lại"
    "Lưu ý đặc biệt:"
    "- Trường 'tinh_trang' chỉ có thể nhận một trong hai giá trị: 'Nhập' hoặc 'Xuất'"
    "- Trường 'ngay' phải được định dạng theo chuẩn: yyyy-mm-dd (VD: 2023-05-15)"
    "Sinh JSON arguments cho function 'generate_search_query'"
)

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4-0613",
    temperature=0
)

# Define function schema for function calling with support for multiple fields and query types
generate_search_query_schema = {
    "name": "generate_search_query",
    "description": "Generate search queries for different field types in MongoDB",
    "parameters": {
        "type": "object",
        "properties": {
            "fuzzy_search": {
                "type": "object",
                "properties": {
                    "ten_hang": {"type": "string", "description": "Search term for ten_hang field using fuzzy match"},
                    "nha_cung_cap": {"type": "string", "description": "Search term for nha_cung_cap field using fuzzy match"}
                }
            },
            "regex_search": {
                "type": "object",
                "properties": {
                    "hs_code": {"type": "string", "description": "Search pattern for hs_code field using regex"}
                }
            },
            "exact_match": {
                "type": "object",
                "properties": {
                    "ngay": {"type": "string", "description": "Exact value for ngay field in yyyy-mm-dd format (e.g., 2023-05-15)"},
                    "luong": {"type": "string", "description": "Exact value for luong field"},
                    "don_vi_tinh": {"type": "string", "description": "Exact value for don_vi_tinh field"},
                    "xuat_xu": {"type": "string", "description": "Exact value for xuat_xu field"},
                    "dieu_kien_giao_hang": {"type": "string", "description": "Exact value for dieu_kien_giao_hang field"},
                    "thue_suat_xnk": {"type": "string", "description": "Exact value for thue_suat_xnk field"},
                    "thue_suat_ttdb": {"type": "string", "description": "Exact value for thue_suat_ttdb field"},
                    "thue_suat_vat": {"type": "string", "description": "Exact value for thue_suat_vat field"},
                    "thue_suat_tu_ve": {"type": "string", "description": "Exact value for thue_suat_tu_ve field"},
                    "thue_suat_bvmt": {"type": "string", "description": "Exact value for thue_suat_bvmt field"},
                    "tinh_trang": {
                        "type": "string", 
                        "description": "Transaction type, only accepts two values: 'Nhập' or 'Xuất'",
                        "enum": ["Nhập", "Xuất"]
                    }
                }
            }
        }
    }
}

# Main function: generate JSON snippet for search
def generate_search_snippet(user_query: str) -> dict:
    messages = [
        SystemMessage(content=template_system),
        HumanMessage(content=user_query)
    ]
    
    # Call LLM with function calling
    response = llm.invoke(
        input=messages,
        tools=[{
            "type": "function",
            "function": generate_search_query_schema
        }],
        tool_choice={"type": "function", "function": {"name": "generate_search_query"}}
    )
    
    # Xử lý tool_calls từ additional_kwargs
    additional_kwargs = getattr(response, "additional_kwargs", {})
    if "tool_calls" in additional_kwargs and additional_kwargs["tool_calls"]:
        tool_call = additional_kwargs["tool_calls"][0]
        if "function" in tool_call and "arguments" in tool_call["function"]:
            return json.loads(tool_call["function"]["arguments"])
    
    # Xử lý tool_calls từ thuộc tính trực tiếp
    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_call = response.tool_calls[0]
        
        # Xử lý nếu tool_call là dict
        if isinstance(tool_call, dict) and "args" in tool_call:
            return tool_call["args"]
        
        # Xử lý nếu tool_call có thuộc tính args
        if hasattr(tool_call, "args"):
            return tool_call.args
    
    # In ra toàn bộ response để debug
    print("Full response object:", response)
    raise ValueError("LLM did not return a valid function call.")

# Build MongoDB query combining Atlas Search and standard query conditions
def build_mongodb_query(search_data):
    pipeline = []
    
    # Process fuzzy search fields (ten_hang and nha_cung_cap)
    fuzzy_fields = search_data.get("fuzzy_search", {})
    fuzzy_conditions = []
    
    # Set default fuzzy parameters
    fuzzy_params = {"maxEdits": 2, "prefixLength": 3, "maxExpansions": 20}
    
    for field, value in fuzzy_fields.items():
        if value:  # Only add non-empty values
            fuzzy_conditions.append({
                "text": {
                    "query": value,
                    "path": field,
                    "fuzzy": fuzzy_params,
                    "score": {"boost": {"value": 1.5}}
                }
            })
    
    # Add $search stage if we have fuzzy conditions
    if fuzzy_conditions:
        # Add the $search stage with score
        pipeline.append({
            "$search": {
                "index": "default",
                "compound": {
                    "should": fuzzy_conditions
                }
            }
        })
        
        # Add stage to keep searchScore in a field
        pipeline.append({
            "$addFields": {
                "searchScore": {"$meta": "searchScore"}
            }
        })
        
        # Create a copy of results to find max score
        pipeline.append({
            "$facet": {
                "results": [],  # Full results with scores
                "maxScore": [
                    {"$sort": {"searchScore": -1}},
                    {"$limit": 1},
                    {"$project": {"maxScore": "$searchScore"}}
                ]
            }
        })
        
        # Compute threshold as 50% of max score and filter
        pipeline.append({
            "$project": {
                "results": {
                    "$filter": {
                        "input": "$results",
                        "as": "item",
                        "cond": {
                            "$gte": [
                                "$$item.searchScore",
                                {"$multiply": [{"$arrayElemAt": ["$maxScore.maxScore", 0]}, 0.5]}
                            ]
                        }
                    }
                }
            }
        })
        
        # Unwind the results back to the main pipeline
        pipeline.append({"$unwind": "$results"})
        pipeline.append({"$replaceRoot": {"newRoot": "$results"}})
    
    # Build $match query for regex and exact matches
    match_conditions = {}
    
    # Process regex search for hs_code
    regex_fields = search_data.get("regex_search", {})
    for field, pattern in regex_fields.items():
        if pattern:  # Only add non-empty values
            match_conditions[field] = {"$regex": pattern, "$options": "i"}
    
    # Process exact match fields
    exact_fields = search_data.get("exact_match", {})
    for field, value in exact_fields.items():
        if value:  # Only add non-empty values
            match_conditions[field] = value
    
    # Add $match stage if we have any conditions
    if match_conditions:
        pipeline.append({
            "$match": match_conditions
        })
    
    # Add a limit to avoid returning too many results
    pipeline.append({"$limit": 100})
    
    return pipeline

# Example usage
if __name__ == "__main__":
    user_input = input("Nhập truy vấn tìm kiếm: ")
    snippet = generate_search_snippet(user_input)
    print("LLM output:")
    print(json.dumps(snippet, ensure_ascii=False, indent=2))
    
    # Build and show the MongoDB pipeline
    mongo_pipeline = build_mongodb_query(snippet)
    print("\nMongoDB Pipeline:")
    print(json.dumps(mongo_pipeline, ensure_ascii=False, indent=2))



#     pipeline=[
#   {
#     "$search": {
#       "index": "default",
#       "compound": {
#         "should": [
#           {
#             "text": {
#               "query": "chim bồ câu",
#               "path": "ten_hang",
#               "fuzzy": {
#                 "maxEdits": 2,
#                 "prefixLength": 3,
#                 "maxExpansions": 100
#               },
#             }
#           },
#           {
#             "text": {
#               "query": "global",
#               "path": "nha_cung_cap",
#               "fuzzy": {
#                 "maxEdits": 2,
#                 "prefixLength": 3,
#                 "maxExpansions": 100
#               },
#             }
#           }
#         ]
#       }
#     }
#   },
#   {
#     "$match": {
#       "tinh_trang": "Nh"
#     }
#   },
#   {
#     "$limit": 10
#   }
# ]
