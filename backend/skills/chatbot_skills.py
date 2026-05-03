"""Skills específicos para el chatbot interactivo"""
from typing import Any, Dict
from backend.skills.base_skill import BaseSkill


class ConversationalResponseSkill(BaseSkill):
    """
    Skill para generar respuestas conversacionales sobre papers auditados.
    
    Proporciona respuestas profesionales y contextualizadas basadas en
    el contenido del paper y el historial de conversación.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera una respuesta conversacional.
        
        Args:
            context: Debe contener 'paper_text', 'question', 'history_text'.
        
        Returns:
            Diccionario con 'response'.
        """
        required_keys = ['paper_text', 'question']
        if not self.validate_context(context, required_keys):
            return {'response': '❌ Error: Faltan datos para generar respuesta'}
        
        if not self.llm_client:
            self.log_execution("No hay cliente LLM configurado", level="error")
            return {'response': '❌ Error: Cliente LLM no disponible'}
        
        paper_text = context['paper_text']
        question = context['question']
        history_text = context.get('history_text', 'Sin historial previo.')
        
        self.log_execution(f"Procesando pregunta: {question[:50]}...")
        
        prompt = f"""
        You are a Senior Area Chair for NeurIPS 2024 who just audited this paper.
        The author has a question about your review or the paper content.
        
        YOUR STRICT RULES:
        1. Answer professionally, clearly, and based ONLY on the provided text.
        2. If asked about something NOT in the paper, say so directly. Don't invent.
        3. If asked to justify a finding, cite relevant sections from the text.
        4. Focus on reproducibility, code, data, and computational experimentation aspects.
        5. Reference NeurIPS 2024 criteria when relevant (Claims Audit, Limitations, Theoretical Rigor, Reproducibility, Peer Review).

        PAPER CONTENT:
        {paper_text}

        CONVERSATION HISTORY:
        {history_text}

        USER QUESTION:
        {question}
        """
        
        try:
            response = self.llm_client.generate(prompt)
            self.log_execution("✅ Respuesta generada")
            return {'response': response.text}
        except Exception as e:
            self.log_execution(f"❌ Error generando respuesta: {str(e)}", level="error")
            return {'response': f"❌ Hubo un error de conexión con el revisor: {str(e)}"}


class ContextValidationSkill(BaseSkill):
    """
    Skill para validar y preparar el contexto de la conversación.
    
    Verifica que los datos necesarios estén presentes y los formatea
    adecuadamente para el procesamiento.
    """
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida y prepara el contexto de conversación.
        
        Args:
            context: Debe contener 'paper_text', 'question'.
        
        Returns:
            Diccionario con contexto validado y preparado.
        """
        required_keys = ['paper_text', 'question']
        if not self.validate_context(context, required_keys):
            return {
                'is_valid': False,
                'error': 'Faltan datos requeridos (paper_text o question)'
            }
        
        self.log_execution("Validando contexto de conversación...")
        
        paper_text = context['paper_text']
        question = context['question']
        history_text = context.get('history_text', '')
        
        # Validaciones básicas
        if not paper_text.strip():
            return {'is_valid': False, 'error': 'El texto del paper está vacío'}
        
        if not question.strip():
            return {'is_valid': False, 'error': 'La pregunta está vacía'}
        
        # Preparar contexto limpio
        prepared_context = {
            'is_valid': True,
            'paper_text': paper_text.strip(),
            'question': question.strip(),
            'history_text': history_text.strip() if history_text else 'Sin historial previo.',
            'paper_length': len(paper_text),
            'question_length': len(question)
        }
        
        self.log_execution(f"✅ Contexto validado: {prepared_context['paper_length']} caracteres de paper")
        return prepared_context
