"""Utilidades para cálculo de puntuaciones"""

def calcular_puntuacion(revision):
    """Calcula la puntuación de reproducibilidad basada en los criterios de revisión"""
    puntos = 0
    aplicables = 0
    
    for item in revision:
        estado = item.get("estado", "").upper()
        if "N/A" in estado or "NO APLICA" in estado or "⚪" in estado:
            continue
        
        if "CUMPLE TOTALMENTE" in estado or "🟢" in estado:
            puntos += 1.0
            aplicables += 1
        elif "CUMPLE MAYORMENTE" in estado or "🔵" in estado:
            puntos += 0.75
            aplicables += 1
        elif "CUMPLE PARCIALMENTE" in estado or "🟡" in estado:
            puntos += 0.5
            aplicables += 1
        elif "CUMPLE MÍNIMAMENTE" in estado or "🟠" in estado:
            puntos += 0.25
            aplicables += 1
        elif "NO CUMPLE" in estado or "🔴" in estado:
            aplicables += 1
    
    if aplicables == 0:
        return 0
    return round((puntos / aplicables) * 100)
