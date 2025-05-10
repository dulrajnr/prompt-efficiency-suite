"""
Domain-Aware Trimmer module for removing redundant tokens while preserving domain-specific terminology.
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

import yaml


@dataclass
class TrimmingResult:
    trimmed_text: str
    original_tokens: int
    trimmed_tokens: int
    preserved_terms: List[str]
    removed_terms: List[str]
    domain: str
    compression_ratio: float


class DomainAwareTrimmer:
    """A class for trimming text while preserving domain-specific terminology."""

    def __init__(self):
        """Initialize the DomainAwareTrimmer."""
        self.domains: Dict[str, Dict[str, Any]] = {}
        self.compound_patterns: Dict[str, List[str]] = {}
        self.tokenization_rules: Dict[str, Dict[str, Any]] = {}

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
                data = json.load(f)
            else:
                data = yaml.safe_load(f)

        self.domains[domain] = {
            "terms": set(data.get("terms", [])),
            "compound_terms": set(data.get("compound_terms", [])),
            "preserve_patterns": data.get("preserve_patterns", []),
            "remove_patterns": data.get("remove_patterns", []),
        }

        # Compile regex patterns
        self.domains[domain]["preserve_regex"] = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.domains[domain]["preserve_patterns"]
        ]
        self.domains[domain]["remove_regex"] = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.domains[domain]["remove_patterns"]
        ]

        # Compile compound term patterns
        self.compound_patterns[domain] = [
            re.compile(re.escape(term), re.IGNORECASE) for term in self.domains[domain]["compound_terms"]
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

    def trim(self, text: str, domain: str, preserve_ratio: float = 0.8) -> TrimmingResult:
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
        tokens = text.split()
        original_tokens = len(tokens)

        # Identify domain terms
        domain_terms = self._identify_domain_terms(text, domain)

        # Apply domain-specific rules
        trimmed_tokens = self._apply_domain_rules(tokens, domain, domain_terms, preserve_ratio)

        # Calculate metrics
        trimmed_text = " ".join(trimmed_tokens)
        trimmed_token_count = len(trimmed_tokens)
        compression_ratio = trimmed_token_count / original_tokens

        # Get preserved and removed terms
        preserved_terms = list(domain_terms)
        removed_terms = [token for token in tokens if token not in trimmed_tokens]

        return TrimmingResult(
            trimmed_text=trimmed_text,
            original_tokens=original_tokens,
            trimmed_tokens=trimmed_token_count,
            preserved_terms=preserved_terms,
            removed_terms=removed_terms,
            domain=domain,
            compression_ratio=compression_ratio,
        )

    def _identify_domain_terms(self, text: str, domain: str) -> Set[str]:
        """Identify domain-specific terms in the text."""
        domain_data = self.domains[domain]
        terms = set()

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
        """Apply domain-specific rules to trim the text."""
        rules = self.tokenization_rules.get(domain, {})
        preserved_tokens = []

        # Calculate minimum tokens to preserve
        min_tokens = int(len(tokens) * preserve_ratio)
        preserved_count = 0

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
                continue

            # Apply custom rules if available
            if self._apply_custom_rules(token, rules):
                preserved_tokens.append(token)
                preserved_count += 1
                continue

            # Preserve tokens to meet minimum ratio
            if preserved_count < min_tokens:
                preserved_tokens.append(token)
                preserved_count += 1

        return preserved_tokens

    def _apply_custom_rules(self, token: str, rules: Dict[str, Any]) -> bool:
        """Apply custom rules to determine if a token should be preserved."""
        if not rules:
            return False

        # Apply custom preservation rules
        if "preserve_if" in rules:
            for condition in rules["preserve_if"]:
                if re.match(condition, token, re.IGNORECASE):
                    return True

        # Apply custom removal rules
        if "remove_if" in rules:
            for condition in rules["remove_if"]:
                if re.match(condition, token, re.IGNORECASE):
                    return False

        return False

    def export_domain_dictionary(self, domain: str, format: str = "json") -> str:
        """Export a domain dictionary to a string.

        Args:
            domain (str): Name of the domain.
            format (str): Output format ('json' or 'yaml').

        Returns:
            str: Serialized domain dictionary.
        """
        if domain not in self.domains:
            raise ValueError(f"Domain '{domain}' not found")

        data = {
            "terms": list(self.domains[domain]["terms"]),
            "compound_terms": list(self.domains[domain]["compound_terms"]),
            "preserve_patterns": self.domains[domain]["preserve_patterns"],
            "remove_patterns": self.domains[domain]["remove_patterns"],
        }

        if format.lower() == "json":
            return json.dumps(data, indent=2)
        else:
            return yaml.dump(data, default_flow_style=False)

    def get_domain_stats(self, domain: str) -> Dict[str, Any]:
        """Get statistics about a domain.

        Args:
            domain (str): Name of the domain.

        Returns:
            Dict[str, Any]: Domain statistics.
        """
        if domain not in self.domains:
            raise ValueError(f"Domain '{domain}' not found")

        return {
            "total_terms": len(self.domains[domain]["terms"]),
            "compound_terms": len(self.domains[domain]["compound_terms"]),
            "preserve_patterns": len(self.domains[domain]["preserve_patterns"]),
            "remove_patterns": len(self.domains[domain]["remove_patterns"]),
        }
