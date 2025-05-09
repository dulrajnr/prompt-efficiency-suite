"""Test that all imports work correctly."""

def test_imports():
    """Test that all required classes can be imported."""
    from prompt_efficiency_suite import (
        DomainAwareTrimmer,
        AdaptiveBudgeting,
        CICDIntegration
    )
    
    # Create instances to verify the classes work
    domain_aware_trimmer = DomainAwareTrimmer()
    adaptive_budgeting = AdaptiveBudgeting()
    cicd_integration = CICDIntegration() 