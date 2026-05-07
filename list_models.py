import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("No se encontró GOOGLE_API_KEY")
    exit()

client = genai.Client(api_key=GOOGLE_API_KEY)
print("Modelos de embedding disponibles:")
try:
    for m in client.models.list():
        print(f"ID: {m.name} | Display Name: {m.display_name}")
except Exception as e:
    print(f"Error listando modelos: {e}")
