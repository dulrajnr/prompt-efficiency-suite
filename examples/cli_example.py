"""
Example usage of the Prompt Efficiency Suite CLI.
"""

from pathlib import Path
import json
import tempfile
import subprocess
import time

def create_sample_files():
    """Create sample files for demonstration."""
    # Create sample input text
    input_text = """
    This is a sample API documentation that needs to be optimized.
    The API provides endpoints for user management and authentication.
    Each request requires an API key for authentication.
    The response format is JSON with status codes and error messages.
    Rate limiting is enforced to prevent abuse.
    """
    
    # Create sample domain dictionary
    domain_dict = {
        'terms': [
            'API', 'endpoint', 'request', 'response', 'authentication',
            'JSON', 'status', 'error', 'rate', 'limit'
        ],
        'compound_terms': [
            'API key', 'rate limiting', 'error message', 'status code'
        ],
        'preserve_patterns': [
            r'[A-Z]{2,}',  # Uppercase acronyms
            r'https?://\S+'  # URLs
        ],
        'remove_patterns': [
            r'TODO',
            r'FIXME',
            r'NOTE:'
        ]
    }
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(input_text)
        input_path = f.name
        
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(domain_dict, f, indent=2)
        domain_path = f.name
        
    return input_path, domain_path

def main():
    """Run CLI examples."""
    # Create sample files
    input_path, domain_path = create_sample_files()
    output_path = 'trimmed_output.txt'
    
    print("Prompt Efficiency Suite CLI Examples")
    print("===================================")
    
    # Example 1: Trim text
    print("\n1. Trimming text with domain awareness:")
    subprocess.run([
        'python', '-m', 'prompt_efficiency_suite.cli',
        'trim', 'trim-text',
        input_path,
        output_path,
        '--domain', domain_path,
        '--preserve-ratio', '0.8'
    ])
    
    # Example 2: Show budget metrics
    print("\n2. Showing budget metrics:")
    subprocess.run([
        'python', '-m', 'prompt_efficiency_suite.cli',
        'budget', 'show-metrics',
        '--config', 'examples/budget_config.json'
    ])
    
    # Example 3: Reset metrics
    print("\n3. Resetting metrics for GPT-4:")
    subprocess.run([
        'python', '-m', 'prompt_efficiency_suite.cli',
        'budget', 'reset-metrics',
        '--config', 'examples/budget_config.json',
        '--model', 'gpt-4'
    ])
    
    # Example 4: Run tests
    print("\n4. Running test suite:")
    subprocess.run([
        'python', '-m', 'prompt_efficiency_suite.cli',
        'cicd', 'run-tests',
        '--config', 'examples/cicd_config.json'
    ])
    
    # Example 5: Deploy package
    print("\n5. Deploying package to PyPI:")
    subprocess.run([
        'python', '-m', 'prompt_efficiency_suite.cli',
        'cicd', 'deploy',
        '--config', 'examples/cicd_config.json',
        '--target', 'pypi'
    ])
    
    # Clean up
    Path(input_path).unlink()
    Path(domain_path).unlink()
    if Path(output_path).exists():
        Path(output_path).unlink()

if __name__ == "__main__":
    main() 