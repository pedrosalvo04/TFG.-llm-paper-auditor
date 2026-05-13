import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

contents = ["hello", "world", "test"]
try:
    res = client.models.embed_content(
        model="gemini-embedding-2",
        contents=contents
    )
    print("Normal embed_content length:", len(res.embeddings) if hasattr(res, 'embeddings') else "no attribute")
except Exception as e:
    print("embed_content error:", e)

try:
    # Let's try what we had: maybe we need to pass it differently
    pass
except Exception as e:
    pass
