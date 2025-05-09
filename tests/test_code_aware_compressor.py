import pytest
from prompt_efficiency_suite.code_aware_compressor import CodeAwareCompressor, CompressionResult

@pytest.fixture
def compressor():
    return CodeAwareCompressor()

@pytest.fixture
def sample_json():
    return '''
    {
        "name": "Test",
        "version": "1.0.0",
        "description": "A test JSON file",
        "dependencies": {
            "package1": "^1.0.0",
            "package2": "^2.0.0"
        },
        "scripts": {
            "test": "pytest",
            "build": "python setup.py build"
        }
    }
    '''

@pytest.fixture
def sample_yaml():
    return '''
    name: Test
    version: 1.0.0
    description: A test YAML file
    dependencies:
      package1: ^1.0.0
      package2: ^2.0.0
    scripts:
      test: pytest
      build: python setup.py build
    '''

@pytest.fixture
def sample_python():
    return '''
    def test_function():
        """
        This is a test function with a docstring.
        """
        # This is a comment
        result = 0
        for i in range(10):
            result += i
        return result
    '''

@pytest.fixture
def sample_markdown():
    return '''
    # Test Document
    
    This is a test document with some **markdown** formatting.
    
    ## Section 1
    
    - Item 1
    - Item 2
    
    ```python
    def test():
        pass
    ```
    '''

def test_compress_json(compressor, sample_json):
    result = compressor.compress(sample_json, 'json')
    
    assert isinstance(result, CompressionResult)
    assert result.content_type == 'json'
    assert result.compression_ratio > 0
    assert result.original_size > result.compressed_size
    assert result.metadata is not None
    assert 'json_depth' in result.metadata
    assert 'json_key_count' in result.metadata

def test_compress_yaml(compressor, sample_yaml):
    result = compressor.compress(sample_yaml, 'yaml')
    
    assert isinstance(result, CompressionResult)
    assert result.content_type == 'yaml'
    assert result.compression_ratio > 0
    assert result.original_size > result.compressed_size
    assert result.metadata is not None
    assert 'yaml_depth' in result.metadata
    assert 'yaml_key_count' in result.metadata

def test_compress_python(compressor, sample_python):
    result = compressor.compress(sample_python, 'python')
    
    assert isinstance(result, CompressionResult)
    assert result.content_type == 'python'
    assert result.compression_ratio > 0
    assert result.original_size > result.compressed_size
    assert result.metadata is not None
    assert 'line_count' in result.metadata
    assert 'word_count' in result.metadata

def test_compress_markdown(compressor, sample_markdown):
    result = compressor.compress(sample_markdown, 'markdown')
    
    assert isinstance(result, CompressionResult)
    assert result.content_type == 'markdown'
    assert result.compression_ratio > 0
    assert result.original_size > result.compressed_size
    assert result.metadata is not None
    assert 'line_count' in result.metadata
    assert 'word_count' in result.metadata

def test_content_type_detection(compressor, sample_json, sample_yaml, sample_python, sample_markdown):
    # Test JSON detection
    result = compressor.compress(sample_json)
    assert result.content_type == 'json'
    
    # Test YAML detection
    result = compressor.compress(sample_yaml)
    assert result.content_type == 'yaml'
    
    # Test Python detection
    result = compressor.compress(sample_python)
    assert result.content_type == 'python'
    
    # Test Markdown detection
    result = compressor.compress(sample_markdown)
    assert result.content_type == 'markdown'

def test_compression_preserves_structure(compressor, sample_json, sample_yaml):
    # Test JSON structure preservation
    json_result = compressor.compress(sample_json, 'json')
    compressed_json = json_result.compressed_content
    assert '{' in compressed_json
    assert '}' in compressed_json
    assert '"name"' in compressed_json
    
    # Test YAML structure preservation
    yaml_result = compressor.compress(sample_yaml, 'yaml')
    compressed_yaml = yaml_result.compressed_content
    assert 'name:' in compressed_yaml
    assert 'dependencies:' in compressed_yaml

def test_compression_metadata(compressor, sample_json, sample_yaml, sample_python):
    # Test JSON metadata
    json_result = compressor.compress(sample_json, 'json')
    assert json_result.metadata['json_depth'] > 0
    assert json_result.metadata['json_key_count'] > 0
    
    # Test YAML metadata
    yaml_result = compressor.compress(sample_yaml, 'yaml')
    assert yaml_result.metadata['yaml_depth'] > 0
    assert yaml_result.metadata['yaml_key_count'] > 0
    
    # Test Python metadata
    python_result = compressor.compress(sample_python, 'python')
    assert python_result.metadata['line_count'] > 0
    assert python_result.metadata['word_count'] > 0
    assert python_result.metadata['character_count'] > 0

def test_compression_ratio(compressor, sample_json, sample_yaml, sample_python, sample_markdown):
    # Test compression ratios for different content types
    json_result = compressor.compress(sample_json, 'json')
    yaml_result = compressor.compress(sample_yaml, 'yaml')
    python_result = compressor.compress(sample_python, 'python')
    markdown_result = compressor.compress(sample_markdown, 'markdown')
    
    assert 0 < json_result.compression_ratio < 1
    assert 0 < yaml_result.compression_ratio < 1
    assert 0 < python_result.compression_ratio < 1
    assert 0 < markdown_result.compression_ratio < 1 