"""Utilidades para cálculo de puntuaciones"""

def calcular_puntuacion(revision):
    """Calcula la puntuación de reproducibilidad basada en los criterios de revisión"""
    puntos = 0
    aplicables = 0
    
    for item in revision:
        estado = item.get("estado", "").strip()
        
        # Saltar N/A
        if "N/A" in estado or "NO APLICA" in estado or "⚪" in estado or "\u26aa" in estado:
            continue
        
        # CUMPLE TOTALMENTE - 100%
        if "CUMPLE TOTALMENTE" in estado or "🟢" in estado or "\u2705" in estado or "✅" in estado:
            puntos += 1.0
            aplicables += 1
        # CUMPLE MAYORMENTE - 75%
        elif "CUMPLE MAYORMENTE" in estado or "🔵" in estado or "\ud83d\udd35" in estado:
            puntos += 0.75
            aplicables += 1
        # CUMPLE PARCIALMENTE - 50%
        elif "CUMPLE PARCIALMENTE" in estado or "🟡" in estado or "\ud83d\udfe1" in estado:
            puntos += 0.5
            aplicables += 1
        # CUMPLE MÍNIMAMENTE - 25%
        elif "CUMPLE MÍNIMAMENTE" in estado or "CUMPLE MINIMAMENTE" in estado or "🟠" in estado or "\ud83d\udfe0" in estado:
            puntos += 0.25
            aplicables += 1
        # NO CUMPLE - 0%
        elif "NO CUMPLE" in estado or "🔴" in estado or "\ud83d\udd34" in estado:
            puntos += 0.0
            aplicables += 1
    
    if aplicables == 0:
        return 0
    
    porcentaje = round((puntos / aplicables) * 100)
    return porcentaje
