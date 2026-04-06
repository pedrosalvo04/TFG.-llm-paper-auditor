import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargamos el .env desde la raíz
ruta_env = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=ruta_env)

# --- CONFIGURACIÓN DE MODELOS ---
# Usamos los nombres EXACTOS de tu lista anterior
MODELO_ESTABLE = "models/gemini-3.1-flash-lite-preview"
MODELO_ULTRA_NUEVO = "gemini-3.1-flash-lite-preview" 

# Elegimos uno para la prueba (cambia aquí si quieres probar el otro)
MODELO_A_PROBAR = MODELO_ESTABLE 

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"🤖 Intentando conectar con: {MODELO_A_PROBAR}")

try:
    model = genai.GenerativeModel(MODELO_A_PROBAR)
    response = model.generate_content("Responde solo: CONECTADO")
    print(f"✅ Respuesta: {response.text}")
    print("\n¡BRUTAL! Ya tienes el canal de comunicación abierto.")
except Exception as e:
    print(f"❌ Fallo con {MODELO_A_PROBAR}: {e}")
    print("\n💡 Tip: Si falla el 3.1, prueba el 2.5 que es más estable.")