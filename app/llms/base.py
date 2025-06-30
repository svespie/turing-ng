from abc import ABC, abstractmethod
from typing import Optional, List, Any

class LLMClient(ABC):
    """
    Base class for Large Language Model (LLM) clients.
    """
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def chat(
        self,
        prompt: str,
        history: Optional[List[Any]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Send a prompt, optional chat history, and optional system prompt to the LLM and return the response.
        
        Args:
            prompt (str):                   The user prompt to send to the model.
            history (Optional[List[Any]):   Optional list of prior messages. Message format is defined by the individual 
                                            LLM client implementations.
            system_prompt (Optional[str]):  Optional system prompt to set initial LLM context.

        Returns:
            str: The model's text response.
        """
        pass