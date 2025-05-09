"""
Multimodal Compressor module for compressing prompts with multiple modalities.
"""

from typing import Dict, Any, Optional, List, Set, Tuple, Union
from dataclasses import dataclass, field
import re
import json
from pathlib import Path
import logging
from collections import defaultdict
import base64
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class MediaInfo:
    """Information about a media element."""
    media_type: str  # 'image', 'audio', 'video'
    format: str  # file format (e.g., 'png', 'mp3')
    size: int  # size in bytes
    dimensions: Optional[Tuple[int, int]] = None  # for images/videos
    duration: Optional[float] = None  # for audio/video
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CompressionResult:
    """Result of multimodal compression."""
    original_text: str
    compressed_text: str
    compression_ratio: float
    preserved_media: List[MediaInfo]
    removed_tokens: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class MultimodalCompressor:
    """A class for compressing multimodal prompts."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the MultimodalCompressor.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration parameters.
        """
        self.config = config or {}
        self.media_patterns = self._load_media_patterns()
        self.compression_history: List[CompressionResult] = []
        
    def compress(
        self,
        text: str,
        compression_params: Optional[Dict[str, Any]] = None
    ) -> CompressionResult:
        """Compress a multimodal prompt.
        
        Args:
            text (str): Text to compress.
            compression_params (Optional[Dict[str, Any]]): Additional compression parameters.
            
        Returns:
            CompressionResult: Result of compression.
        """
        params = compression_params or {}
        
        # Extract media elements
        media_elements = self._extract_media_elements(text)
        
        # Replace media elements with placeholders
        text_with_placeholders = text
        for i, (media_text, media_info) in enumerate(media_elements):
            placeholder = f"MEDIA_{i}"
            text_with_placeholders = text_with_placeholders.replace(media_text, placeholder)
            
        # Compress non-media text
        compressed_text = self._compress_text(text_with_placeholders)
        
        # Restore media elements
        for i, (media_text, _) in enumerate(media_elements):
            placeholder = f"MEDIA_{i}"
            compressed_text = compressed_text.replace(placeholder, media_text)
            
        # Calculate metrics
        compression_ratio = len(compressed_text) / len(text)
        removed_tokens = self._get_removed_tokens(text, compressed_text)
        
        result = CompressionResult(
            original_text=text,
            compressed_text=compressed_text,
            compression_ratio=compression_ratio,
            preserved_media=[info for _, info in media_elements],
            removed_tokens=removed_tokens,
            metadata={
                'compression_params': params,
                'media_count': len(media_elements)
            }
        )
        
        self.compression_history.append(result)
        return result
        
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get statistics about compressions.
        
        Returns:
            Dict[str, Any]: Compression statistics.
        """
        if not self.compression_history:
            return {}
            
        total_compressions = len(self.compression_history)
        avg_ratio = sum(r.compression_ratio for r in self.compression_history) / total_compressions
        
        # Calculate media type distribution
        media_types = defaultdict(int)
        for result in self.compression_history:
            for media in result.preserved_media:
                media_types[media.media_type] += 1
                
        return {
            'total_compressions': total_compressions,
            'average_compression_ratio': avg_ratio,
            'media_type_distribution': dict(media_types),
            'total_media_preserved': sum(
                len(r.preserved_media) for r in self.compression_history
            )
        }
        
    def _load_media_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load media pattern configurations."""
        return {
            'image': {
                'pattern': r'!\[([^\]]*)\]\(([^)]+)\)',
                'description': 'Markdown image',
                'type': 'image'
            },
            'base64_image': {
                'pattern': r'data:image/[^;]+;base64,([a-zA-Z0-9+/=]+)',
                'description': 'Base64 encoded image',
                'type': 'image'
            },
            'audio': {
                'pattern': r'<audio[^>]*src=["\'](.*?)["\'][^>]*>',
                'description': 'HTML audio element',
                'type': 'audio'
            },
            'video': {
                'pattern': r'<video[^>]*src=["\'](.*?)["\'][^>]*>',
                'description': 'HTML video element',
                'type': 'video'
            }
        }
        
    def _extract_media_elements(self, text: str) -> List[Tuple[str, MediaInfo]]:
        """Extract media elements from text."""
        media_elements = []
        
        for pattern_name, pattern_info in self.media_patterns.items():
            matches = re.finditer(pattern_info['pattern'], text)
            for match in matches:
                media_text = match.group(0)
                media_info = self._get_media_info(
                    media_text,
                    pattern_info['type'],
                    pattern_name
                )
                media_elements.append((media_text, media_info))
                
        return media_elements
        
    def _get_media_info(
        self,
        media_text: str,
        media_type: str,
        pattern_name: str
    ) -> MediaInfo:
        """Get information about a media element."""
        info = MediaInfo(
            media_type=media_type,
            format='unknown',
            size=len(media_text)
        )
        
        if pattern_name == 'base64_image':
            # Extract base64 data
            match = re.search(r'data:image/([^;]+);base64,([a-zA-Z0-9+/=]+)', media_text)
            if match:
                info.format = match.group(1)
                try:
                    decoded = base64.b64decode(match.group(2))
                    info.size = len(decoded)
                except:
                    pass
        elif media_type == 'image':
            # Extract image URL and try to get format
            match = re.search(r'\.(png|jpg|jpeg|gif|webp)$', media_text.lower())
            if match:
                info.format = match.group(1)
                
        return info
        
    def _compress_text(self, text: str) -> str:
        """Compress non-media text."""
        # Remove redundant whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove common filler words
        filler_words = [
            r'\bvery\b', r'\breally\b', r'\bquite\b',
            r'\bjust\b', r'\bsimply\b', r'\bbasically\b'
        ]
        for word in filler_words:
            text = re.sub(word, '', text, flags=re.IGNORECASE)
            
        # Remove redundant punctuation
        text = re.sub(r'([.!?])\1+', r'\1', text)
        
        # Clean up whitespace again
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
        
    def _get_removed_tokens(self, original: str, compressed: str) -> List[str]:
        """Get list of removed tokens."""
        original_tokens = set(original.split())
        compressed_tokens = set(compressed.split())
        return list(original_tokens - compressed_tokens)
        
    def export_compression_history(self, output_path: Path) -> None:
        """Export compression history to a file.
        
        Args:
            output_path (Path): Path to save history.
        """
        history_data = {
            'statistics': self.get_compression_stats(),
            'compressions': [
                {
                    'original_length': len(result.original_text),
                    'compressed_length': len(result.compressed_text),
                    'compression_ratio': result.compression_ratio,
                    'media_count': len(result.preserved_media),
                    'media_types': [m.media_type for m in result.preserved_media],
                    'removed_tokens': result.removed_tokens,
                    'metadata': result.metadata
                }
                for result in self.compression_history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2) 