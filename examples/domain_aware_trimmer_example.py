"""
Example usage of the DomainAwareTrimmer class.
"""

from prompt_efficiency_suite import DomainAwareTrimmer
from pathlib import Path

def main():
    # Initialize the trimmer
    trimmer = DomainAwareTrimmer()
    
    # Load the API domain dictionary
    domain_path = Path("examples/domains/api_domain.json")
    trimmer.load_domain("api", domain_path)
    
    # Set custom tokenization rules
    trimmer.set_tokenization_rules("api", {
        "preserve_pos": ["NOUN", "VERB", "PROPN"],
        "min_length": 3,
        "remove_stop_words": True
    })
    
    # Example API documentation text
    text = """
    TODO: Update the REST API documentation by 2024-03-20.
    
    The API endpoint /api/v1/users supports the following operations:
    1. GET /api/v1/users - List all users
    2. POST /api/v1/users - Create a new user
    3. GET /api/v1/users/{id} - Get user by ID
    4. PUT /api/v1/users/{id} - Update user
    5. DELETE /api/v1/users/{id} - Delete user
    
    Authentication is required using a Bearer token in the Authorization header.
    Rate limiting is set to 100 requests per minute.
    
    FIXME: Add error response examples.
    """
    
    # Trim the text while preserving domain terms
    result = trimmer.trim(text, "api", preserve_ratio=0.8)
    
    # Print results
    print("Original text:")
    print(text)
    print("\nTrimmed text:")
    print(result.trimmed_text)
    print("\nMetrics:")
    print(f"Original tokens: {result.original_tokens}")
    print(f"Trimmed tokens: {result.trimmed_tokens}")
    print(f"Compression ratio: {result.compression_ratio:.2f}")
    print("\nPreserved terms:")
    print(", ".join(result.preserved_terms))
    print("\nRemoved terms:")
    print(", ".join(result.removed_terms))
    
    # Export domain dictionary
    print("\nDomain dictionary (JSON):")
    print(trimmer.export_domain_dictionary("api", format="json"))
    
    # Get domain statistics
    print("\nDomain statistics:")
    stats = trimmer.get_domain_stats("api")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main() 