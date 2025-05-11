"""Domain Aware Trimmer - A module for trimming prompts based on domain-specific rules."""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern, Set, TypedDict, Union

import yaml

logger = logging.getLogger(__name__)


@dataclass
class TrimmingResult:
    """Result of domain-aware trimming."""

    trimmed_text: str
    original_tokens: int
    trimmed_tokens: int
    preserved_terms: List[str]
    removed_terms: List[str]
    domain: str
    compression_ratio: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class DomainConfig(TypedDict):
    """Configuration for a domain."""

    terms: Set[str]
    compound_terms: Set[str]
    preserve_patterns: List[str]
    remove_patterns: List[str]
    preserve_regex: List[Pattern[str]]
    remove_regex: List[Pattern[str]]


class DomainAwareTrimmer:
    """A class for trimming text while preserving domain-specific terminology."""

    def __init__(self):
        """Initialize the DomainAwareTrimmer."""
        self.domains: Dict[str, DomainConfig] = {}
        self.compound_patterns: Dict[str, List[Pattern[str]]] = {}
        self.tokenization_rules: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)

    def load_domain(self, domain: str, dictionary_path: Union[str, Path]) -> None:
        """Load a domain-specific dictionary.

        Args:
            domain (str): Name of the domain (e.g., 'legal', 'medical').
            dictionary_path (Union[str, Path]): Path to the dictionary file (JSON or YAML).
        """
        path = Path(dictionary_path)
        if not path.exists():
            raise FileNotFoundError(f"Dictionary file not found: {dictionary_path}")

        with open(path, "r", encoding="utf-8") as f:
            if path.suffix.lower() == ".json":
                data: Dict[str, Any] = json.load(f)
            else:
                data: Dict[str, Any] = yaml.safe_load(f)

        self.domains[domain] = {
            "terms": set(data.get("terms", [])),
            "compound_terms": set(data.get("compound_terms", [])),
            "preserve_patterns": data.get("preserve_patterns", []),
            "remove_patterns": data.get("remove_patterns", []),
            "preserve_regex": [
                re.compile(pattern, re.IGNORECASE)
                for pattern in data.get("preserve_patterns", [])
            ],
            "remove_regex": [
                re.compile(pattern, re.IGNORECASE)
                for pattern in data.get("remove_patterns", [])
            ],
        }

        # Compile compound term patterns
        self.compound_patterns[domain] = [
            re.compile(re.escape(term), re.IGNORECASE)
            for term in self.domains[domain]["compound_terms"]
        ]

    def add_domain_terms(self, domain: str, terms: List[str]) -> None:
        """Add terms to an existing domain dictionary.

        Args:
            domain (str): Name of the domain.
            terms (List[str]): List of terms to add.
        """
        if domain not in self.domains:
            self.domains[domain] = {
                "terms": set(),
                "compound_terms": set(),
                "preserve_patterns": [],
                "remove_patterns": [],
                "preserve_regex": [],
                "remove_regex": [],
            }

        self.domains[domain]["terms"].update(terms)

    def set_tokenization_rules(self, domain: str, rules: Dict[str, Any]) -> None:
        """Set tokenization rules for a domain.

        Args:
            domain (str): Name of the domain.
            rules (Dict[str, Any]): Tokenization rules.
        """
        self.tokenization_rules[domain] = rules

    def trim(
        self, text: str, domain: str, preserve_ratio: float = 0.8
    ) -> TrimmingResult:
        """Trim text while preserving domain-specific terminology.

        Args:
            text (str): Text to trim.
            domain (str): Domain to use for trimming.
            preserve_ratio (float): Minimum ratio of domain terms to preserve.

        Returns:
            TrimmingResult: Result containing trimmed text and metrics.
        """
        if domain not in self.domains:
            raise ValueError(f"Domain '{domain}' not loaded")

        # Tokenize text using simple whitespace splitting
        tokens: List[str] = text.split()
        original_tokens: int = len(tokens)

        # Identify domain terms
        domain_terms: Set[str] = self._identify_domain_terms(text, domain)

        # Apply domain-specific rules
        trimmed_tokens: List[str] = self._apply_domain_rules(
            tokens, domain, domain_terms, preserve_ratio
        )

        # Calculate metrics
        trimmed_text: str = " ".join(trimmed_tokens)
        trimmed_token_count: int = len(trimmed_tokens)
        compression_ratio: float = trimmed_token_count / original_tokens

        # Get preserved and removed terms
        preserved_terms: List[str] = list(domain_terms)
        removed_terms: List[str] = [
            token for token in tokens if token not in trimmed_tokens
        ]

        return TrimmingResult(
            trimmed_text=trimmed_text,
            original_tokens=original_tokens,
            trimmed_tokens=trimmed_token_count,
            preserved_terms=preserved_terms,
            removed_terms=removed_terms,
            domain=domain,
            compression_ratio=compression_ratio,
            metadata={"timestamp": self._get_timestamp()},
        )

    def _identify_domain_terms(self, text: str, domain: str) -> Set[str]:
        """Identify domain-specific terms in the text.

        Args:
            text (str): Text to analyze.
            domain (str): Domain to use for identification.

        Returns:
            Set[str]: Set of identified domain terms.
        """
        domain_data: DomainConfig = self.domains[domain]
        terms: Set[str] = set()

        # Check for exact matches (case-insensitive)
        for term in domain_data["terms"]:
            if re.search(re.escape(term), text, re.IGNORECASE):
                terms.add(term)

        # Check for compound terms
        for pattern in self.compound_patterns[domain]:
            matches = pattern.finditer(text)
            for match in matches:
                terms.add(match.group())

        # Check for pattern matches
        for pattern in domain_data["preserve_regex"]:
            matches = pattern.finditer(text)
            terms.update(match.group() for match in matches)

        return terms

    def _apply_domain_rules(
        self,
        tokens: List[str],
        domain: str,
        domain_terms: Set[str],
        preserve_ratio: float,
    ) -> List[str]:
        """Apply domain-specific rules to trim the text.

        Args:
            tokens (List[str]): List of tokens to process.
            domain (str): Domain to use for rules.
            domain_terms (Set[str]): Set of domain terms to preserve.
            preserve_ratio (float): Minimum ratio of tokens to preserve.

        Returns:
            List[str]: List of preserved tokens.
        """
        rules: Dict[str, Any] = self.tokenization_rules.get(domain, {})
        preserved_tokens: List[str] = []

        # Calculate minimum tokens to preserve
        min_tokens: int = int(len(tokens) * preserve_ratio)
        preserved_count: int = 0

        # First pass: preserve domain terms and their context
        for i, token in enumerate(tokens):
            # Always preserve domain terms and their immediate context
            if any(term.lower() in token.lower() for term in domain_terms):
                # Add previous token for context if available
                if i > 0 and tokens[i - 1] not in preserved_tokens:
                    preserved_tokens.append(tokens[i - 1])
                    preserved_count += 1

                # Add the domain term
                preserved_tokens.append(token)
                preserved_count += 1

                # Add next token for context if available
                if i < len(tokens) - 1 and tokens[i + 1] not in preserved_tokens:
                    preserved_tokens.append(tokens[i + 1])
                    preserved_count += 1

        # Second pass: apply custom rules
        for token in tokens:
            if token not in preserved_tokens and self._apply_custom_rules(token, rules):
                preserved_tokens.append(token)
                preserved_count += 1

            # Stop if we've preserved enough tokens
            if preserved_count >= min_tokens:
                break

        return preserved_tokens

    def _apply_custom_rules(self, token: str, rules: Dict[str, Any]) -> bool:
        """Apply custom tokenization rules.

        Args:
            token (str): Token to process.
            rules (Dict[str, Any]): Rules to apply.

        Returns:
            bool: True if token should be preserved.
        """
        # Check minimum length
        min_length: int = rules.get("min_length", 3)
        if len(token) < min_length:
            return False

        # Check for stop words
        stop_words: Set[str] = set(rules.get("stop_words", []))
        if token.lower() in stop_words:
            return False

        # Check for special characters
        special_chars: Set[str] = set(rules.get("special_chars", []))
        if any(char in token for char in special_chars):
            return False

        return True

    def export_domain_dictionary(self, domain: str, format: str = "json") -> str:
        """Export domain dictionary to a string.

        Args:
            domain (str): Domain to export.
            format (str): Output format ('json' or 'yaml').

        Returns:
            str: Exported dictionary as string.
        """
        if domain not in self.domains:
            raise ValueError(f"Domain '{domain}' not loaded")

        data: Dict[str, Any] = {
            "terms": list(self.domains[domain]["terms"]),
            "compound_terms": list(self.domains[domain]["compound_terms"]),
            "preserve_patterns": self.domains[domain]["preserve_patterns"],
            "remove_patterns": self.domains[domain]["remove_patterns"],
            "metadata": {"timestamp": self._get_timestamp()},
        }

        if format.lower() == "json":
            return json.dumps(data, indent=2)
        elif format.lower() == "yaml":
            return yaml.dump(data, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def get_domain_stats(self, domain: str) -> Dict[str, Any]:
        """Get statistics about a domain.

        Args:
            domain (str): Domain to get stats for.

        Returns:
            Dict[str, Any]: Domain statistics.
        """
        if domain not in self.domains:
            raise ValueError(f"Domain '{domain}' not loaded")

        return {
            "terms_count": len(self.domains[domain]["terms"]),
            "compound_terms_count": len(self.domains[domain]["compound_terms"]),
            "preserve_patterns_count": len(self.domains[domain]["preserve_patterns"]),
            "remove_patterns_count": len(self.domains[domain]["remove_patterns"]),
            "metadata": {"timestamp": self._get_timestamp()},
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            str: ISO format timestamp.
        """
        return datetime.now().isoformat()
