"""Sistema de logging centralizado con soporte de colores"""
import logging
import sys

# Códigos de colores ANSI
class Colors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

class ColoredFormatter(logging.Formatter):
    """Formateador personalizado para añadir colores según nivel y contenido"""
    
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    LEVEL_COLORS = {
        logging.DEBUG: Colors.BLUE,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.BOLD + Colors.RED,
    }

    def format(self, record):
        log_fmt = self.FORMAT
        
        # Color especial para peticiones HTTP
        if "HTTP Request" in record.msg:
            color = Colors.CYAN
            record.msg = f"{color}{record.msg}{Colors.RESET}"
        else:
            color = self.LEVEL_COLORS.get(record.levelno, Colors.RESET)
            # Solo coloreamos el nivel para no saturar
            record.levelname = f"{color}{record.levelname}{Colors.RESET}"
            
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def get_logger(name):
    """Obtiene un logger configurado con colores"""
    logger = logging.getLogger(name)
    logger.propagate = False # Evitar duplicados con el root
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    # Silenciar logs internos verbosos
    logging.getLogger("google_genai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.INFO)
    
    return logger
