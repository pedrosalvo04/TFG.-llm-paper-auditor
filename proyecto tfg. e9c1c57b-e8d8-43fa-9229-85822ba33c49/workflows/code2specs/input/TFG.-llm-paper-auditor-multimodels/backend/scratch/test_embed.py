import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

contents = ["hello", "world", "test"]
res = client.models.embed_content(
    model="gemini-embedding-2",
    contents=contents
)

print(f"Type of res: {type(res)}")
if hasattr(res, 'embeddings'):
    print(f"Type of embeddings: {type(res.embeddings)}")
    if isinstance(res.embeddings, list):
        print(f"Length of embeddings: {len(res.embeddings)}")
        print(f"Type of first embedding: {type(res.embeddings[0])}")
        print(f"Type of first embedding values: {type(res.embeddings[0].values)}")
        print(f"Length of first embedding values: {len(res.embeddings[0].values)}")
    else:
        print(f"Embeddings is not a list. It is {type(res.embeddings)}")
else:
    print("No embeddings attribute")
