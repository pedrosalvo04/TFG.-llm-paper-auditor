"""Clase base para todos los skills de los agentes IA"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from backend.common.llm_client import LLMClient
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class BaseSkill(ABC):
    """
    Clase base abstracta para definir skills de agentes IA.
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None, config: Optional[Dict] = None):
        self.llm_client = llm_client
        self.config = config or {}
        self.name = self.__class__.__name__
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def validate_context(self, context: Dict[str, Any], required_keys: list) -> bool:
        missing_keys = [key for key in required_keys if key not in context]
        if missing_keys:
            logger.error(f"Skill '{self.name}': Faltan claves en contexto: {missing_keys}")
            return False
        return True
    
    def log_execution(self, message: str, level: str = "info"):
        """
        Registra un mensaje de ejecución del skill con soporte para colores.
        """
        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'notice': 25,  # Nivel naranja
            'warning': logging.WARNING,
            'error': logging.ERROR
        }
        
        log_level = levels.get(level.lower(), logging.INFO)
        # Obtener el logger específico de la clase que está ejecutando
        cls_logger = get_logger(self.__class__.__module__)
        full_message = f"[{self.name}] {message}"
        cls_logger.log(log_level, full_message)


class CompositeSkill(BaseSkill):
    def __init__(self, skills: list[BaseSkill], llm_client: Optional[LLMClient] = None):
        super().__init__(llm_client)
        self.skills = skills
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
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
