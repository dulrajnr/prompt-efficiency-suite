import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import re
import base64
from PIL import Image
import io

class MultimodalCompressor:
    def __init__(self):
        self.original_tokens = 0
        self.compressed_tokens = 0
        self.Image = Image
        self.io = io
    
    def compress(self, content: str, content_type: str = 'text') -> str:
        """Compress content based on its type."""
        if content_type == 'json':
            return self._compress_json(content)
        elif content_type in ['yaml', 'yml']:
            return self._compress_yaml(content)
        elif content_type == 'python':
            return self._compress_python(content)
        elif content_type == 'image':
            return self._compress_image(content)
        else:
            return self._compress_text(content)
    
    def _compress_json(self, content: str) -> str:
        """Compress JSON content."""
        try:
            data = json.loads(content)
            # Remove unnecessary whitespace
            compressed = json.dumps(data, separators=(',', ':'))
            self._update_token_counts(content, compressed)
            return compressed
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON content")
    
    def _compress_yaml(self, content: str) -> str:
        """Compress YAML content."""
        try:
            data = yaml.safe_load(content)
            # Convert to JSON for better compression
            compressed = json.dumps(data, separators=(',', ':'))
            self._update_token_counts(content, compressed)
            return compressed
        except yaml.YAMLError:
            raise ValueError("Invalid YAML content")
    
    def _compress_python(self, content: str) -> str:
        """Compress Python code."""
        # Remove comments and unnecessary whitespace
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Preserve docstrings
                if not (line.startswith('"""') or line.startswith("'''")):
                    lines.append(line)
        
        compressed = ' '.join(lines)
        self._update_token_counts(content, compressed)
        return compressed
    
    def _compress_image(self, content: str) -> str:
        """Compress image content."""
        try:
            # Decode base64 image
            image_data = base64.b64decode(content)
            image = self.Image.open(self.io.BytesIO(image_data))
            
            # Compress image
            output = self.io.BytesIO()
            image.save(output, format='JPEG', quality=60, optimize=True)
            compressed_data = output.getvalue()
            
            # Encode back to base64
            compressed = base64.b64encode(compressed_data).decode()
            self._update_token_counts(content, compressed)
            return compressed
        except Exception as e:
            raise ValueError(f"Image compression failed: {str(e)}")
    
    def _compress_text(self, content: str) -> str:
        """Compress text content."""
        # Basic text compression: remove extra whitespace
        compressed = ' '.join(content.split())
        self._update_token_counts(content, compressed)
        return compressed
    
    def _update_token_counts(self, original: str, compressed: str) -> None:
        """Update token counts for compression ratio calculation."""
        self.original_tokens = len(original)
        self.compressed_tokens = len(compressed)
    
    def get_compression_ratio(self) -> float:
        """Calculate compression ratio."""
        if self.original_tokens == 0:
            return 1.0
        return self.compressed_tokens / self.original_tokens 