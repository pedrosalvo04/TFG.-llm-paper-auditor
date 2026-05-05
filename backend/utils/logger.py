"""Sistema de logging centralizado con soporte de colores"""
import logging
import sys

# Registrar nivel personalizado para extracciones
logging.addLevelName(25, "NOTICE")

# Colores ANSI para la consola
class Colors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"
    ORANGE = "\033[95m" # Cambiado a Magenta para visibilidad máxima
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

class ColoredFormatter(logging.Formatter):
    """Formateador de logs con colores según el nivel"""
    
    FORMATS = {
        logging.DEBUG: f"{Colors.CYAN}%(asctime)s - %(name)s - DEBUG - %(message)s{Colors.RESET}",
        logging.INFO: f"{Colors.GREEN}%(asctime)s - %(message)s{Colors.RESET}",
        25: f"{Colors.ORANGE}%(asctime)s - %(message)s{Colors.RESET}",
        logging.WARNING: f"{Colors.YELLOW}%(asctime)s - %(levelname)s - %(message)s{Colors.RESET}",
        logging.ERROR: f"{Colors.RED}%(asctime)s - ERROR - %(message)s{Colors.RESET}",
        logging.CRITICAL: f"{Colors.BOLD}{Colors.RED}%(asctime)s - CRITICAL - %(message)s{Colors.RESET}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def get_logger(name):
    """
    Obtiene un logger configurado con colores y formato limpio.
    Garantiza que el handler con colores esté presente.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Permitir todo el flujo, el handler filtrará
    
    # Limpiar handlers previos para evitar duplicados o formatos incorrectos
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    
    # Crear nuestro handler con ColoredFormatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter())
    logger.addHandler(handler)
    
    # IMPORTANTE: No propagar al logger raíz de Streamlit que suele romper el formato
    logger.propagate = False
    
    return logger
