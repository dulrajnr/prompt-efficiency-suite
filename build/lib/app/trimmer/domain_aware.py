from typing import Dict, List, Optional
import tiktoken
from pathlib import Path
import json
import logging
import os
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DomainAwareTrimmer:
    def __init__(self, dictionary_path: str = "data/dicts"):
        # Handle relative paths
        self.dictionary_path = Path(dictionary_path).resolve()
        logger.debug(f"Dictionary path set to: {self.dictionary_path}")
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.domain_dictionaries: Dict[str, Dict[str, float]] = {}
        
    def load_domain_dictionary(self, domain: str) -> None:
        """Load a domain-specific dictionary from file."""
        dict_path = self.dictionary_path / f"{domain}.json"
        logger.debug(f"Attempting to load dictionary from: {dict_path}")
        if dict_path.exists():
            logger.debug(f"Dictionary file found at: {dict_path}")
            with open(dict_path, 'r') as f:
                self.domain_dictionaries[domain] = json.load(f)
                logger.debug(f"Loaded {len(self.domain_dictionaries[domain])} terms for domain {domain}")
        else:
            logger.error(f"Dictionary file not found at: {dict_path}")
            # Try current working directory as fallback
            cwd_path = Path.cwd() / "data/dicts" / f"{domain}.json"
            logger.debug(f"Trying fallback path: {cwd_path}")
            if cwd_path.exists():
                logger.debug(f"Dictionary file found at fallback path: {cwd_path}")
                with open(cwd_path, 'r') as f:
                    self.domain_dictionaries[domain] = json.load(f)
                    logger.debug(f"Loaded {len(self.domain_dictionaries[domain])} terms for domain {domain}")
    
    def find_important_spans(self, text: str, domain: str, min_importance: float = 0.7) -> List[tuple[int, int]]:
        """Find spans of text that contain important domain terms."""
        important_spans = []
        
        # Sort terms by length (longest first) to handle overlapping matches
        terms = sorted(self.domain_dictionaries[domain].items(), key=lambda x: len(x[0]), reverse=True)
        
        # Find all occurrences of each term
        for term, importance in terms:
            if importance >= min_importance:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                for match in pattern.finditer(text):
                    important_spans.append((match.start(), match.end()))
        
        # Sort spans by start position
        important_spans.sort()
        
        # Merge overlapping spans
        if not important_spans:
            return []
            
        merged = [important_spans[0]]
        for current in important_spans[1:]:
            previous = merged[-1]
            if current[0] <= previous[1]:
                # Spans overlap, merge them
                merged[-1] = (previous[0], max(previous[1], current[1]))
            else:
                merged.append(current)
        
        return merged
    
    def trim_prompt(self, prompt: str, domain: str, min_importance: float = 0.7) -> str:
        """Trim a prompt while preserving important domain-specific terms."""
        if domain not in self.domain_dictionaries:
            logger.debug(f"Loading dictionary for domain: {domain}")
            self.load_domain_dictionary(domain)
            
        if domain not in self.domain_dictionaries:
            raise ValueError(f"Domain dictionary not found for {domain}")
        
        # Find important spans
        important_spans = self.find_important_spans(prompt, domain, min_importance)
        logger.debug(f"Found {len(important_spans)} important spans")
        
        # Extract and join important spans
        important_parts = [prompt[start:end] for start, end in important_spans]
        trimmed_text = " ".join(important_parts)
        
        return trimmed_text
    
    def get_token_count(self, prompt: str) -> int:
        """Get the token count for a prompt."""
        return len(self.enc.encode(prompt)) 