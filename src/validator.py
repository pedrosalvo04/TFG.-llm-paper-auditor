import os
from pathlib import Path
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Cargamos el .env desde la raíz del proyecto (un nivel arriba de src/)
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


class PaperAuditor:
    def __init__(self):
        self.model_name = "gemini-3.1-flash-lite-preview"
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # Configuramos el modelo para que SIEMPRE responda en JSON
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"response_mime_type": "application/json"}
        )

    def audit(self, paper_text):
        prompt = f"""
        Actúa como un Auditor Editorial de Nature Portfolio. 
        Evalúa el manuscrito frente a TODOS los puntos de la 'Reporting Summary'.
        
        CRITERIOS A EVALUAR:
        1. Estadística: Informar n, tests, significancia y si son tests de una o dos colas.
        2. Software y Código: Disponibilidad, versiones y repositorios (GitHub/Zenodo).
        3. Disponibilidad de Datos: Declaración de acceso y DOIs de los datasets.
        4. Diseño Experimental: Tamaño de muestra, exclusión de datos, aleatorización y cegamiento (blinding).
        5. Materiales (Si aplica): Validación de anticuerpos, líneas celulares y autenticación.
        6. Ética y Humanos (Si aplica): Consentimiento informado, comité de ética y datos clínicos.
        7. Reproducibilidad: Detalles suficientes de la metodología.

        INSTRUCCIÓN DE SALIDA:
        Devuelve EXCLUSIVAMENTE un objeto JSON con esta estructura:
        {{
          "revision": [
            {{
              "categoria": "Nombre de la categoría",
              "estado": "✅ CUMPLE / ⚠️ PARCIAL / ❌ NO CUMPLE / ⚪ N/A",
              "hallazgo": "Breve explicación basada en el texto",
              "recomendacion": "Qué debe añadir el autor"
            }}
          ],
          "veredicto_final": "Resumen general"
        }}

        TEXTO DEL ARTÍCULO:
        {paper_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}