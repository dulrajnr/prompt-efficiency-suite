"""
Example usage of the Prompt Efficiency Suite REST API.
"""

import requests
import json
import tempfile
from pathlib import Path
import time

# API configuration
BASE_URL = "http://localhost:8000"
USERNAME = "test"
PASSWORD = "test"

def get_access_token():
    """Get access token for authentication."""
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": USERNAME, "password": PASSWORD}
    )
    response.raise_for_status()
    return response.json()["access_token"]

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
    
    # Create temporary domain dictionary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(domain_dict, f, indent=2)
        domain_path = f.name
        
    return input_text, domain_path

def main():
    """Run API examples."""
    print("Prompt Efficiency Suite API Examples")
    print("===================================")
    
    try:
        # Get access token
        print("\n1. Getting access token...")
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ Access token obtained")
        
        # Create sample files
        input_text, domain_path = create_sample_files()
        
        # Example 1: Trim text
        print("\n2. Trimming text with domain awareness...")
        response = requests.post(
            f"{BASE_URL}/trim",
            headers=headers,
            json={
                "text": input_text,
                "domain": domain_path,
                "preserve_ratio": 0.8
            }
        )
        response.raise_for_status()
        trim_result = response.json()
        print("Original tokens:", trim_result["original_tokens"])
        print("Trimmed tokens:", trim_result["trimmed_tokens"])
        print("Compression ratio:", f"{trim_result['compression_ratio']:.2%}")
        print("Preserved terms:", len(trim_result["preserved_terms"]))
        print("✓ Text trimmed successfully")
        
        # Example 2: Get budget metrics
        print("\n3. Getting budget metrics...")
        response = requests.get(
            f"{BASE_URL}/budget/metrics",
            headers=headers
        )
        response.raise_for_status()
        metrics = response.json()
        for model_metrics in metrics:
            print(f"\n{model_metrics['model']}:")
            print(f"Total tokens: {model_metrics['total_tokens']:,}")
            print(f"Total cost: ${model_metrics['total_cost']:.2f}")
            print(f"Requests: {model_metrics['request_count']}")
        print("✓ Budget metrics retrieved")
        
        # Example 3: Get budget alerts
        print("\n4. Getting budget alerts...")
        response = requests.get(
            f"{BASE_URL}/budget/alerts",
            headers=headers,
            params={"model": "gpt-4"}
        )
        response.raise_for_status()
        alerts = response.json()
        if alerts:
            for alert in alerts:
                print(f"\nAlert at {alert['timestamp']}:")
                print(f"Type: {alert['alert_type']}")
                print(f"Message: {alert['message']}")
        else:
            print("No alerts found")
        print("✓ Budget alerts retrieved")
        
        # Example 4: Run tests
        print("\n5. Running test suite...")
        response = requests.post(
            f"{BASE_URL}/cicd/tests",
            headers=headers
        )
        response.raise_for_status()
        test_result = response.json()
        print(f"Passed tests: {test_result['passed_tests']}")
        print(f"Failed tests: {test_result['failed_tests']}")
        print(f"Coverage: {test_result['coverage']:.1%}")
        print(f"Duration: {test_result['duration']:.2f}s")
        print("✓ Tests completed")
        
        # Example 5: Deploy package
        print("\n6. Deploying package...")
        response = requests.post(
            f"{BASE_URL}/cicd/deploy",
            headers=headers,
            params={"target": "pypi"}
        )
        response.raise_for_status()
        deploy_result = response.json()
        print(f"Status: {deploy_result['status']}")
        print(f"Version: {deploy_result['version']}")
        print(f"Duration: {deploy_result['duration']:.2f}s")
        print("✓ Deployment completed")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up
        if 'domain_path' in locals():
            Path(domain_path).unlink()

if __name__ == "__main__":
    main() 