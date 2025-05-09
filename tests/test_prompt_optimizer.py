"""Test the PromptOptimizer class."""

import pytest
from prompt_efficiency_suite import PromptOptimizer

def test_prompt_optimization():
    """Test basic prompt optimization."""
    optimizer = PromptOptimizer()
    
    # Test prompt with redundant whitespace
    prompt = """
    This is a test   prompt    with
    redundant    whitespace   and
    empty    lines.
    
    It should be optimized.
    """
    
    result = optimizer.optimize(prompt)
    
    # Check that the result is a string
    assert isinstance(result.optimized_prompt, str)
    
    # Check that whitespace is normalized
    assert "  " not in result.optimized_prompt
    
    # Check that length reduction is positive
    assert result.improvement_metrics['length_reduction_ratio'] > 0
    
    # Check that the optimized prompt is more concise
    assert len(result.optimized_prompt) < len(result.original_prompt)

def test_optimization_with_params():
    """Test optimization with custom parameters."""
    optimizer = PromptOptimizer()
    
    prompt = "This is a test prompt."
    params = {
        'apply_remove_redundant_whitespace': False,
        'apply_remove_empty_lines': False
    }
    
    result = optimizer.optimize(prompt, params)
    
    # Check that parameters are respected
    assert result.metadata['optimization_params'] == params
    
def test_optimization_stats():
    """Test optimization statistics."""
    optimizer = PromptOptimizer()
    
    # Optimize multiple prompts
    prompts = [
        "First test prompt",
        "Second test prompt",
        "Third test prompt"
    ]
    
    for prompt in prompts:
        optimizer.optimize(prompt)
        
    stats = optimizer.get_optimization_stats()
    
    # Check that stats are calculated correctly
    assert stats['total_prompts'] == len(prompts)
    assert 'average_token_reduction' in stats
    assert 'average_execution_time' in stats
    assert 'average_improvements' in stats 