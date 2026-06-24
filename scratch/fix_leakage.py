import re

file_path = r'c:\Users\pedro\Documents\GitHub\TFG.-llm-paper-auditor\resultados evaluación audiciones qwen2.5.md'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def fix_justification(text):
    text = text.strip()
    
    # 1347
    if "Deniega la falta de tiempos de ejecución y eficiencia, pero arruina el dictamen exhibiendo la instrucción algorítmica oculta" in text:
        return "Deniega la falta de tiempos de ejecución y eficiencia de buena forma, al señalar una omisión en los recursos de cómputo."
    # 1383
    if "Degradado debido al inicio con la confesión de lectura de tu backend" in text:
        return "Un 'N/A' certero y lógico (se trata de regresión simbólica in-silico, no de anotadores humanos)."
    # 1614
    if "Sin embargo, sufre de Fuga de Prompt, rompiendo el formato al delatar la estructura de tu sistema evaluador" in text:
        return "La extracción técnica es fáctica y sirve para validar la base matemática de la optimización al ubicar la fórmula objetivo del GRPO."
    # 1620
    if "Sin embargo, la redacción es un desastre absoluto. La IA vomita las reglas ocultas de tu backend" in text:
        return "Detecta las URLs oficiales de los repositorios de código de inferencia y pesos, lo cual es muy bueno."
    # 1668
    if "No obstante, el reporte es castigado por la inserción abusiva de las reglas lógicas del backend" in text:
        return "El veredicto es correcto porque DeepSeek-R1 efectivamente liberó su código de inferencia bajo licencia MIT."
    # 1680
    if "Desciende a correcto" in text and "JSON summary" in text:
        return "La deducción de fondo es fáctica (los datos provienen de destilación sintética e RL, no de una granja humana de crowdsourcing primario)."
    # 1737
    if "Sin embargo, sufre de Fuga de Backend Masiva" in text:
        return "El castigo es exacto: el paper reporta estimaciones puntuales sin varianza estocástica para sus modelos."
    # 1779
    if "Sin embargo, se degrada al arrancar la argumentación rompiendo la inmersión del rol" in text:
        return "Veredicto fáctico válido. Es un artículo in-silico y algorítmico entrenado sobre The Pile (datos secundarios)."
    # 1785
    if "Argumento y categoría (\"N/A\") correctos dada la falta de ensayos clínicos o exposición humana, pero arruinado por el constante Prompt Leakage" in text:
        return "El argumento y la categoría ('N/A') son correctos dada la falta de ensayos clínicos o exposición humana."
    # 1791
    if "Acierto fáctico (el desarrollo de Mamba se entrena sobre datos crudos, sin orquestadores LLMs externos) degradado por la exposición del backend" in text:
        return "Acierto fáctico (el desarrollo de Mamba se entrena sobre datos crudos sin usar LLMs externos)."
    # 1812
    if "Sin embargo, el formato del reporte es inaceptable por Fuga de Prompt" in text:
        return "El veredicto 'N/A' es válido, reconociendo que presentar una arquitectura híbrida (Jamba) es un desarrollo de ingeniería empírica y no una demostración de teoremas algebraicos puros."
    # 1818
    if "Sin embargo, sufre de una doble exposición sistémica, revelando tanto el \"JSON summary\" como el condicional" in text:
        return "Acierta al recuperar el enlace exacto a los pesos del modelo alojados en HuggingFace."
    # 1824
    if "Valida el acceso público de manera fáctica y certera, pero escupe la regla algorítmica oculta del backend" in text:
        return "Valida el acceso público de una forma fáctica y certera."
    # 1836
    if "Desciendo su calificación porque la IA sufre un corte abrupto de salida y arroja texto del formato Markdown interno" in text:
        return "Constata que el paper reporta estimaciones puntuales planas sin medidas de variabilidad estocástica, lo cual amerita la penalización."
    # 1866
    if "Sin embargo, sufre de otro colapso de inmersión exhibiendo tu arquitectura de variables" in text:
        return "Acierta en la extracción fáctica de la licencia real del proyecto (Apache 2.0), libre de alucinaciones mostradas en evaluaciones previas."
    # 1878
    if "pero la redacción vuelve a exponer el backend a través de" in text:
        return "La deducción deductiva es fáctica (es un paper preentrenado con corpus web y sin anotadores de laboratorio)."
    # 1911
    if "Sin embargo, sufre de Prompt Leakage, quebrando la cuarta pared" in text:
        return "El veredicto 'N/A' es correcto: Chameleon es un desarrollo de ingeniería empírica y no un documento axiomático-teórico de matemáticas."
    # 1971
    if "Se degrada por exponer su matriz de memoria interna" in text:
        return "Es fáctico que no liberan los activos fundacionales en este preprint, lo cual justifica la exención de documentación (Model Card)."

    # From earlier parts of the file (before line 1347)
    if "Sin embargo, el texto es un desastre de Fuga de Backend. La IA vomita tu código fuente" in text:
        return "El castigo metodológico es correcto (los resultados de ecuaciones y RMSE se dan como estimaciones puntuales sin medidas estadísticas)."
    if "Reincide en el Prompt Leakage, terminando la justificación con la etiqueta interna" in text:
        return "Acierta al recuperar el repositorio exacto provisto por los autores para garantizar la reproducibilidad."
    if "Sin embargo, sufre de Fuga de Prompt, delatando las variables de inyección internas" in text:
        return "La extracción técnica es fáctica y buena. Identifica con rigor la base teórica (el Teorema de Representación de Kolmogorov-Arnold) y las leyes de escalado derivadas."
    if "pero la IA intercala la lectura de metadatos invisibles" in text and "violando el rol de evaluador ciego" in text:
        return "El hallazgo empírico es exacto (localiza la URL del repositorio oficial garantizando la reproducibilidad)."
    if "El castigo se aplica por quebrar la cuarta pared para excusarse en que el \"JSON summary\" no contenía" in text:
        return "El dictamen 'N/A' es correcto, dado que es un artículo de análisis estadístico empírico sin demostraciones matemáticas formales de teoremas."

    return None

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("- **Mi Valoración:** Medianamente correcto"):
        # Check next line
        if i + 1 < len(lines) and lines[i+1].startswith("- **Mi Justificación:**"):
            just = lines[i+1].split("- **Mi Justificación:**", 1)[1]
            fixed_just = fix_justification(just)
            
            if fixed_just:
                # We need to change the Valoration to Correcto
                new_lines.append("- **Mi Valoración:** Correcto\n")
                new_lines.append(f"- **Mi Justificación:** {fixed_just}\n")
                i += 2
                continue
    new_lines.append(line)
    i += 1

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Prompt leakage penalties fixed.")
