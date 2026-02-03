from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from pydantic import BaseModel, Field, ConfigDict

# --- Data Models ---

class InteractionRequest(BaseModel):
    """
    Standardized request object for the LLM interaction.
    """
    prompt: str = Field(..., description="The user prompt or input text.")
    system_prompt: Optional[str] = Field(None, description="Optional system instruction.")
    model_name: str = Field(..., description="Target model to use (e.g., 'llama3').")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Generation temperature.")
    max_tokens: int = Field(1024, gt=0, description="Max tokens to generate.")
    request_id: str = Field(..., description="Unique ID for tracing.")
    
    model_config = ConfigDict(extra="ignore")

class InteractionResponse(BaseModel):
    """
    Standardized response object from the LLM interaction.
    """
    content: str = Field(..., description="The generated text content.")
    raw_response: Dict[str, Any] = Field(default_factory=dict, description="Raw provider response.")
    token_usage: Optional[Dict[str, int]] = Field(None, description="Token usage stats.")
    finish_reason: Optional[str] = Field(None, description="Why generation stopped.")
    
    model_config = ConfigDict(extra="ignore")

class VerificationResult(BaseModel):
    """
    Result from a single verifier or aggregated verification.
    """
    passed: bool
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1.")
    errors: List[str] = Field(default_factory=list, description="List of validation errors found.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extra verification details.")

# --- Protocols / Interfaces ---

@runtime_checkable
class AbstractGenerator(Protocol):
    """
    Protocol for LLM Providers (Ollama, vLLM, OpenAI, etc.)
    """
    @abstractmethod
    async def generate(self, request: InteractionRequest) -> InteractionResponse:
        """
        Generate a solitary response (non-streaming).
        """
        ...
    
    @abstractmethod
    async def generate_stream(self, request: InteractionRequest):
        """
        Generate a streaming response (yields chunks).
        # Return type annotation omitted for complexity, but implies AsyncIterator[str]
        """
        ...

@runtime_checkable
class AbstractVerifier(Protocol):
    """
    Protocol for Validation Logic (Safety, Schema, Instruction, etc.)
    """
    @abstractmethod
    async def verify(self, request: InteractionRequest, response: InteractionResponse) -> VerificationResult:
        """
        Run the verification check.
        """
        ...

@runtime_checkable
class AbstractHealer(Protocol):
    """
    Protocol for Self-Healing Strategies.
    """
    @abstractmethod
    async def heal(self, failed_request: InteractionRequest, failure_reason: VerificationResult) -> InteractionRequest:
        """
        Modify the request to attempt a fix based on the failure reason.
        """
        ...

@runtime_checkable
class AbstractRouter(Protocol):
    """
    Protocol for Routing Logic.
    """
    @abstractmethod
    async def route(self, request: InteractionRequest) -> str:
        """
        Determine which model/provider to use for this request.
        Returns the model_name.
        """
        ...
