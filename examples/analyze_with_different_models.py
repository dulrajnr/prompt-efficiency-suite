#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different models.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_with_model(analyzer, prompt, model):
    """Analyze a prompt with a specific model and print the results."""
    print(f"\nAnalyzing with {model.value}:")
    print("=" * 50)
    
    result = analyzer.analyze_prompt(
        prompt=prompt,
        model=model
    )
    
    print("\nAnalysis Results:")
    print(f"Clarity Score: {result.metrics.clarity_score:.2f}")
    print(f"Structure Score: {result.metrics.structure_score:.2f}")
    print(f"Complexity Score: {result.metrics.complexity_score:.2f}")
    print(f"Token Estimate: {result.metrics.token_estimate}")
    print(f"Quality Score: {result.metrics.quality_score:.2f}")
    
    print("\nTop Improvement Suggestions:")
    for suggestion in result.metrics.improvement_suggestions[:3]:
        print(f"- {suggestion}")

async def main():
    # Initialize the analyzer
    analyzer = PromptAnalyzer()
    
    # Example prompts
    prompts = {
        "Simple Prompt": """
        Help me write a function to add two numbers.
        """,
        
        "Complex Prompt": """
        Given the intricate nature of quantum mechanics and its implications on
        string theory, please provide a comprehensive analysis of how these
        concepts relate to general relativity, taking into account the various
        mathematical frameworks and theoretical models that have been proposed.
        """,
        
        "Well-Structured Prompt": """
        System: You are a helpful assistant.
        Context: This is some background information about the task.
        Instruction: Please help me with this task step by step.
        Example: Here's how to do it.
        """
    }
    
    # Test each prompt with different models
    for description, prompt in prompts.items():
        print(f"\n{description}:")
        print("-" * 30)
        print(f"Prompt:\n{prompt}")
        
        for model in ModelType:
            await analyze_with_model(analyzer, prompt, model)
            print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 