import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

# Load environment variables
load_dotenv()
MONGODB_URI = os.environ.get("MONGODB_URI")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize MongoDB client
def get_mongo_collection(db_name: str, collection_name: str):
    client = MongoClient(MONGODB_URI)
    db = client[db_name]
    return db[collection_name]

# Initialize OpenAI client
llm = OpenAI(api_key=OPENAI_API_KEY)

# Define Function Schema for OpenAI
generate_search_query_schema = {
    "name": "generate_search_query",
    "description": "Sinh snippet JSON cho stage $search của MongoDB Atlas Search",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Nội dung tìm kiếm từ người dùng"},
            "path": {"type": "string", "description": "Tên trường cần tìm"},
            "fuzzy": {
                "type": "object",
                "properties": {
                    "maxEdits": {"type": "integer"},
                    "prefixLength": {"type": "integer"},
                    "maxExpansions": {"type": "integer"}
                },
                "required": ["maxEdits", "prefixLength", "maxExpansions"]
            }
        },
        "required": ["query", "path", "fuzzy"]
    }
}

# Few-shot examples for prompt
system_prompt = """
Bạn là chuyên gia MongoDB Atlas Search. Sinh JSON argument cho function 'generate_search_query'.
Output chỉ JSON function call, không text khác.

Example 1:
User: Tìm gà sống
AI:
{ "name": "generate_search_query", "arguments": {"query":"gà sống","path":"ten_hang","fuzzy":{"maxEdits":1,"prefixLength":1,"maxExpansions":20}} }

Example 2:
User: HS code 0105 và Hyline
AI:
{ "name": "generate_search_query", "arguments": {"query":"0105 Hyline","path":"hs_code","fuzzy":{"maxEdits":1,"prefixLength":2,"maxExpansions":30}} }

User: {input}
AI:
"""

def run_search_agent(user_input: str, db_name: str = "project230255", collection_name: str = "hs_code"):
    # 1) Generate function call via LLM
    response = llm.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": system_prompt.replace('{input}', user_input)},
            {"role": "user", "content": user_input}
        ],
        functions=[generate_search_query_schema],
        function_call={"name": "generate_search_query"}
    )
    message = response.choices[0].message
    func_call = message.function_call
    args = json.loads(func_call.arguments)

    # 2) Build MongoDB pipeline
    search_stage = {"$search": {"text": args}}
    pipeline = [
        search_stage,
        {"$set": {"score": {"$meta": "searchScore"}}},
        {"$limit": 20}
    ]

    # 3) Execute pipeline
    coll = get_mongo_collection(db_name, collection_name)
    results = list(coll.aggregate(pipeline))

    # 4) Return results
    return results

# Example usage
if __name__ == "__main__":
    query = input("Nhập truy vấn tìm kiếm: ")
    docs = run_search_agent(query)
    for doc in docs:
        print(doc)
