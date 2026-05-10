"""Clase base para todos los skills de los agentes IA"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from backend.common.llm_client import LLMClient
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class BaseSkill(ABC):
    """
    Clase base abstracta para definir skills de agentes IA.
    
    Un skill representa una capacidad específica que puede ser ejecutada
    por un agente IA, como extraer información, evaluar criterios, o
    generar respuestas.
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None, config: Optional[Dict] = None):
        """
        Inicializa el skill base.
        
        Args:
            llm_client: Cliente LLM configurado. Si no se proporciona, el skill
                       debe crear uno propio o no usar LLM.
            config: Diccionario con configuración específica del skill.
        """
        self.llm_client = llm_client
        self.config = config or {}
        self.name = self.__class__.__name__
        logger.debug(f"Skill '{self.name}' inicializado")
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta el skill con el contexto proporcionado.
        
        Args:
            context: Diccionario con toda la información necesaria para ejecutar el skill.
                    Puede incluir: paper_text, extracted_info, red_flags, etc.
        
        Returns:
            Diccionario con los resultados de la ejecución del skill.
        """
        pass
    
    def validate_context(self, context: Dict[str, Any], required_keys: list) -> bool:
        """
        Valida que el contexto contenga todas las claves requeridas.
        
        Args:
            context: Contexto a validar.
            required_keys: Lista de claves requeridas.
        
        Returns:
            True si todas las claves están presentes, False en caso contrario.
        """
        missing_keys = [key for key in required_keys if key not in context]
        if missing_keys:
            logger.error(f"Skill '{self.name}': Faltan claves en contexto: {missing_keys}")
            return False
        return True
    
    def log_execution(self, message: str, level: str = "info"):
        """
        Registra un mensaje de ejecución del skill.
        
        Args:
            message: Mensaje a registrar.
            level: Nivel de log (info, warning, error).
        """
        full_message = f"[{self.name}] {message}"
        if level == "info":
            logger.info(full_message)
        elif level == "warning":
            logger.warning(full_message)
        elif level == "error":
            logger.error(full_message)
        else:
            logger.debug(full_message)


class CompositeSkill(BaseSkill):
    """
    Skill compuesto que ejecuta múltiples skills en secuencia.
    
    Permite orquestar varios skills para realizar tareas complejas,
    pasando el contexto de uno a otro.
    """
    
    def __init__(self, skills: list[BaseSkill], llm_client: Optional[LLMClient] = None):
        """
        Inicializa el skill compuesto.
        
        Args:
            skills: Lista de skills a ejecutar en secuencia.
            llm_client: Cliente LLM opcional para los skills.
        """
        super().__init__(llm_client)
        self.skills = skills
        self.log_execution(f"Skill compuesto con {len(skills)} skills")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta todos los skills en secuencia, acumulando resultados.
        
        Args:
            context: Contexto inicial.
        
        Returns:
            Contexto actualizado con los resultados de todos los skills.
        """
        accumulated_context = context.copy()
        
        for i, skill in enumerate(self.skills, 1):
            self.log_execution(f"Ejecutando skill {i}/{len(self.skills)}: {skill.name}")
            try:
                result = skill.execute(accumulated_context)
                accumulated_context.update(result)
            except Exception as e:
                self.log_execution(f"Error en skill {skill.name}: {str(e)}", level="error")
                accumulated_context[f"error_{skill.name}"] = str(e)
        
        return accumulated_context
