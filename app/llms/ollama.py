import requests

from typing import Optional, List, Dict, TypedDict, Any
from app.llms.base import LLMClient
from app.llms.registry import register_llm
from app.core.exceptions import HostVerificationError, ModelVerificationError, ChatResponseError

DEFAULT_URL: str = "http://localhost:11434"

class OllamaMessage(TypedDict):
    role: str       # 'system', 'user', 'assistant'
    content: str    # message text

@register_llm("ollama")
class OllamaLLM(LLMClient):
    f"""
    LLM client for interacting with an Ollama server.

    By default, connects to a local instance ({DEFAULT_URL}), but
    can connect to any accessible Ollama API endpoint.
    """
    def __init__(self, model: str, host: Optional[str] = DEFAULT_URL) -> None:
        f"""
        Initialize an OllamaLLM client.

        Args:
            model (str):            The name of the Ollama model to use (e.g., 'mistral:latest').
                                    Must correstpond to a model available on the target Ollama server.
            host (Optional[str]):   The base URL for the Ollama API. Defaults to '{DEFAULT_URL}',
                                    which is the standard location for local/self-hosted Ollama instances.
                                    For remote instances, provide the appropriate URL.

        Raises:
            HostVerificationError:  If the Ollama server is unreachable or otherwise unavailable.
            ModelVerificationError: If the Ollama model is not installed or otherwise unavailable.
            
        Note:
            This constructor does not handle Ollama installation. The server must be running and accessible to use this class.
        """
        if not model:
            raise ModelVerificationError("Model is required for OllamaLLM.")
        self.model = model
        self.host = host.rstrip("/")
        if not self.host:
            raise HostVerificationError(f"Host {host} is invalid.")
        self._verify_server()
        self._verify_model()
    
    def _verify_server(self) -> None:
        """
        Checks if the Ollama server is reachable.

        Raises:
            HostVerificationError:  If the Ollama server is unreachable.
        """
        try:
            response = requests.get(f"{self.host}/v1/models", timeout=2)
            response.raise_for_status()
            self.available_models: Optional[List[str]] = [model["id"] for model in response.json().get("data",[])]
        except Exception as ex:
            raise HostVerificationError(f"Ollama server {self.host} unreachable: {ex}")

    def _verify_model(self) -> None:
        """
        Checks if the Ollama model is available.
        """
        if not self.available_models:
            raise ModelVerificationError(
                f"The server {self.host} did not return any available models.\n"
                f"Use 'ollama pull <model>' to download one."
            )
        if self.model not in self.available_models:
            raise ModelVerificationError(
                f"Model {self.model} not available at {self.host}.\n"
                f"Available models: {', '.join(self.available_models)}\n"
                f"Use 'ollama pull {self.model.split(':')[0]}' to download."
            )
        
    def chat(
            self,
            prompt: str,
            history: Optional[List[OllamaMessage]] = None,
            system_prompt: Optional[str] = None
    ) -> tuple[str, List[OllamaMessage]]:
        """
        Sends a prompt to the Ollama model and return its response.
        This method also allows for optional history and system prompt for context.

        Args:
            prompt (str):                               The user prompt to send to the model.
            history (Optional[List[OllamaMessage]]):    Optional list of prior messages.
            system_prompt (Optional[str]):              Optional system prompt to set initial LLM context.

        Returns:
            tuple[str, List[OllamaMessage]]: The LLM response text and update chat history.
        """
        url: str = f"{self.host}/v1/chat/completions"
        messages: List[OllamaMessage] = []
        history = history[:] if history else []
        if system_prompt and (not history[0]["role"] != "system"):
            system_message = OllamaMessage(role="system", content=system_prompt)
            messages.append(system_message)
        if history:
            messages.extend(history)
        new_message: OllamaMessage = OllamaMessage(role="user", content=prompt)
        messages.append(new_message)
        payload: Dict[str, Any] = { "model": self.model, "messages": messages }
        response: requests.Response = requests.post(url, json=payload)
        response.raise_for_status()
        llm_response: str = response.json()["choices"][0]["message"]["content"] or ""
        response_message: OllamaMessage = OllamaMessage(role="assistant", content="llm_response")
        history.append(new_message)
        history.append(response_message)
        return llm_response, history
