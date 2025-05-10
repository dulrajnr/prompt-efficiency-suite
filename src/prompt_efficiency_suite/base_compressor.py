from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

import tiktoken
from pydantic import BaseModel


class CompressionResult(BaseModel):
    """Model for storing compression results."""

    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    compressed_text: str
    metadata: Dict[str, Union[str, int, float]]


class BaseCompressor(ABC):
    """Base class for all prompt compressors."""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the compressor with a specific model."""
        self.model_name = model_name
        self.encoding = tiktoken.encoding_for_model(model_name)

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text."""
        return len(self.encoding.encode(text))

    def calculate_compression_ratio(self, original_tokens: int, compressed_tokens: int) -> float:
        """Calculate the compression ratio."""
        if original_tokens == 0:
            return 0.0
        return (original_tokens - compressed_tokens) / original_tokens

    @abstractmethod
    async def compress(self, text: str, target_ratio: Optional[float] = None) -> CompressionResult:
        """Compress the input text.

        Args:
            text: The text to compress
            target_ratio: Optional target compression ratio (0.0 to 1.0)

        Returns:
            CompressionResult containing compression metrics and results
        """
        pass

    @abstractmethod
    async def batch_compress(self, texts: List[str], target_ratio: Optional[float] = None) -> List[CompressionResult]:
        """Compress multiple texts in batch.

        Args:
            texts: List of texts to compress
            target_ratio: Optional target compression ratio (0.0 to 1.0)

        Returns:
            List of CompressionResult objects
        """
        pass
