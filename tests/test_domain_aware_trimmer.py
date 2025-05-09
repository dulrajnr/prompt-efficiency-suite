"""
Test suite for the DomainAwareTrimmer class.
"""

import pytest
from pathlib import Path
import json
import tempfile
from prompt_efficiency_suite.domain_aware_trimmer import DomainAwareTrimmer, TrimmingResult

@pytest.fixture
def trimmer():
    """Create a DomainAwareTrimmer instance for testing."""
    return DomainAwareTrimmer()

@pytest.fixture
def sample_domain_dict():
    """Create a sample domain dictionary for testing."""
    return {
        'terms': ['API', 'endpoint', 'request', 'response'],
        'compound_terms': ['REST API', 'HTTP request', 'JSON response'],
        'preserve_patterns': [r'\b[A-Z]{2,}\b', r'\b\d{4}-\d{2}-\d{2}\b'],
        'remove_patterns': [r'\bTODO\b', r'\bFIXME\b']
    }

@pytest.fixture
def temp_domain_file(sample_domain_dict):
    """Create a temporary domain dictionary file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_domain_dict, f)
        return f.name

def test_load_domain(trimmer, temp_domain_file):
    """Test loading a domain dictionary."""
    trimmer.load_domain('api', temp_domain_file)
    assert 'api' in trimmer.domains
    assert len(trimmer.domains['api']['terms']) == 4
    assert len(trimmer.domains['api']['compound_terms']) == 3
    assert len(trimmer.domains['api']['preserve_patterns']) == 2
    assert len(trimmer.domains['api']['remove_patterns']) == 2

def test_add_domain_terms(trimmer):
    """Test adding terms to a domain dictionary."""
    trimmer.add_domain_terms('api', ['token', 'authentication'])
    assert 'api' in trimmer.domains
    assert 'token' in trimmer.domains['api']['terms']
    assert 'authentication' in trimmer.domains['api']['terms']

def test_set_tokenization_rules(trimmer):
    """Test setting tokenization rules."""
    rules = {
        'preserve_pos': ['NOUN', 'VERB'],
        'min_length': 3,
        'remove_stop_words': True
    }
    trimmer.set_tokenization_rules('api', rules)
    assert 'api' in trimmer.tokenization_rules
    assert trimmer.tokenization_rules['api'] == rules

def test_trim_text(trimmer, temp_domain_file):
    """Test trimming text while preserving domain terms."""
    trimmer.load_domain('api', temp_domain_file)
    
    text = "Make an HTTP request to the REST API endpoint and handle the JSON response"
    result = trimmer.trim(text, 'api')
    
    assert isinstance(result, TrimmingResult)
    assert result.domain == 'api'
    assert result.original_tokens > 0
    assert result.trimmed_tokens > 0
    assert result.compression_ratio <= 1.0
    assert all(term in result.preserved_terms for term in ['API', 'request', 'response'])

def test_trim_with_patterns(trimmer, temp_domain_file):
    """Test trimming with regex patterns."""
    trimmer.load_domain('api', temp_domain_file)
    
    text = "TODO: Update the REST API endpoint by 2024-03-20"
    result = trimmer.trim(text, 'api')
    
    assert 'TODO' not in result.trimmed_text
    assert '2024-03-20' in result.trimmed_text
    assert 'REST API' in result.trimmed_text

def test_trim_with_custom_rules(trimmer, temp_domain_file):
    """Test trimming with custom tokenization rules."""
    trimmer.load_domain('api', temp_domain_file)
    trimmer.set_tokenization_rules('api', {
        'preserve_pos': ['NOUN'],
        'min_length': 4,
        'remove_stop_words': True
    })
    
    text = "The API endpoint should handle the request properly"
    result = trimmer.trim(text, 'api')
    
    assert 'The' not in result.trimmed_text  # Stop word removed
    assert 'API' in result.trimmed_text  # Domain term preserved
    assert 'endpoint' in result.trimmed_text  # Noun preserved

def test_trim_with_preserve_ratio(trimmer, temp_domain_file):
    """Test trimming with different preserve ratios."""
    trimmer.load_domain('api', temp_domain_file)
    
    text = "Make an HTTP request to the REST API endpoint and handle the JSON response"
    
    # Test with high preserve ratio
    result_high = trimmer.trim(text, 'api', preserve_ratio=0.9)
    assert result_high.compression_ratio > 0.9
    
    # Test with low preserve ratio
    result_low = trimmer.trim(text, 'api', preserve_ratio=0.5)
    assert result_low.compression_ratio < result_high.compression_ratio

def test_export_domain_dictionary(trimmer, temp_domain_file):
    """Test exporting domain dictionary."""
    trimmer.load_domain('api', temp_domain_file)
    
    # Test JSON export
    json_export = trimmer.export_domain_dictionary('api', format='json')
    assert isinstance(json_export, str)
    assert 'terms' in json_export
    assert 'API' in json_export
    
    # Test YAML export
    yaml_export = trimmer.export_domain_dictionary('api', format='yaml')
    assert isinstance(yaml_export, str)
    assert 'terms:' in yaml_export
    assert 'API' in yaml_export

def test_get_domain_stats(trimmer, temp_domain_file):
    """Test getting domain statistics."""
    trimmer.load_domain('api', temp_domain_file)
    
    stats = trimmer.get_domain_stats('api')
    assert isinstance(stats, dict)
    assert stats['term_count'] == 4
    assert stats['compound_term_count'] == 3
    assert stats['preserve_pattern_count'] == 2
    assert stats['remove_pattern_count'] == 2

def test_invalid_domain(trimmer):
    """Test operations with invalid domain."""
    with pytest.raises(ValueError):
        trimmer.trim("Some text", "invalid_domain")
        
    with pytest.raises(ValueError):
        trimmer.export_domain_dictionary("invalid_domain")
        
    with pytest.raises(ValueError):
        trimmer.get_domain_stats("invalid_domain")

def test_invalid_dictionary_file(trimmer):
    """Test loading invalid dictionary file."""
    with pytest.raises(FileNotFoundError):
        trimmer.load_domain('api', 'nonexistent.json') 