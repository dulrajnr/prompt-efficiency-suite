#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different models.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, model_name, model_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing Prompt with {model_name} Model:")
    print("=" * 50)
    print(f"Prompt:\n{prompt}")
    
    result = analyzer.analyze_prompt(
        prompt=prompt,
        model=model_type
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
    
    print("\nKey Patterns:")
    for pattern_type, patterns in result.pattern_analysis.items():
        if patterns:
            print(f"\n{pattern_type}:")
            for pattern in patterns[:2]:
                print(f"  - {pattern}")

async def main():
    # Initialize the analyzer
    analyzer = PromptAnalyzer()
    
    # Example prompt
    prompt = """
    System: You are a helpful assistant.
    Context: This is the background information.
    Instruction: Help me with this task.
    Example: Here's an example.
    """
    
    # Example models
    models = {
        "GPT-4": ModelType.GPT4,
        "GPT-3.5": ModelType.GPT35,
        "Claude": ModelType.CLAUDE,
        "PaLM": ModelType.PALM,
        "LLaMA": ModelType.LLAMA,
        "Mistral": ModelType.MISTRAL
    }
    
    # Analyze the prompt with each model
    for model_name, model_type in models.items():
        await analyze_prompt(analyzer, prompt, model_name, model_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 