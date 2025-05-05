"""
Multimodal Compressor module for handling both text and image compression.
"""

from typing import List, Dict, Any, Union
from PIL import Image
import numpy as np
import spacy
import tiktoken
from concurrent.futures import ThreadPoolExecutor

class MultimodalCompressor:
    """A class for compressing both text and image data."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the MultimodalCompressor.
        
        Args:
            model_name (str): The name of the spaCy model to use.
        """
        self.nlp = spacy.load(model_name)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def compress_images(self, images: List[Image.Image]) -> List[Image.Image]:
        """Compress a list of images.
        
        Args:
            images (List[Image.Image]): List of images to compress.
            
        Returns:
            List[Image.Image]: Compressed images.
        """
        with ThreadPoolExecutor() as executor:
            compressed = list(executor.map(self._compress_single_image, images))
        return compressed
    
    def compress_texts(self, texts: List[str]) -> List[str]:
        """Compress a list of texts.
        
        Args:
            texts (List[str]): List of texts to compress.
            
        Returns:
            List[str]: Compressed texts.
        """
        with ThreadPoolExecutor() as executor:
            compressed = list(executor.map(self._compress_single_text, texts))
        return compressed
    
    def compress_multimodal(self, texts: List[str], images: List[Image.Image]) -> List[Dict[str, Any]]:
        """Compress both texts and images together.
        
        Args:
            texts (List[str]): List of texts to compress.
            images (List[Image.Image]): List of images to compress.
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing compressed text and image.
        """
        if len(texts) != len(images):
            raise ValueError("Number of texts and images must be equal")
            
        compressed_texts = self.compress_texts(texts)
        compressed_images = self.compress_images(images)
        
        return [
            {"text": text, "image": img}
            for text, img in zip(compressed_texts, compressed_images)
        ]
    
    def _compress_single_image(self, image: Image.Image) -> Image.Image:
        """Compress a single image.
        
        Args:
            image (Image.Image): Image to compress.
            
        Returns:
            Image.Image: Compressed image.
        """
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Resize if too large
        max_size = (800, 800)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
        # Optimize quality
        return image
    
    def _compress_single_text(self, text: str) -> str:
        """Compress a single text.
        
        Args:
            text (str): Text to compress.
            
        Returns:
            str: Compressed text.
        """
        doc = self.nlp(text)
        
        # Remove stop words and lemmatize
        compressed = " ".join(token.lemma_ for token in doc if not token.is_stop)
        
        # Remove extra whitespace
        compressed = " ".join(compressed.split())
        
        return compressed.strip() 