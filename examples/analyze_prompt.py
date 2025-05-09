#!/usr/bin/env python3
"""
Example script demonstrating how to use the Prompt Efficiency Suite.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def main():
    # Initialize the analyzer
    analyzer = PromptAnalyzer()
    
    # Example prompt
    prompt = """
    System: You are a helpful assistant.
    Context: This is some background information about the task.
    Instruction: Please help me with this task step by step.
    Example: Here's how to do it.
    """
    
    # Analyze the prompt
    result = analyzer.analyze_prompt(
        prompt=prompt,
        model=ModelType.GPT4
    )
    
    # Print results
    print("\nPrompt Analysis Results:")
    print("=" * 50)
    
    print("\nMetrics:")
    print(f"Clarity Score: {result.metrics.clarity_score:.2f}")
    print(f"Structure Score: {result.metrics.structure_score:.2f}")
    print(f"Complexity Score: {result.metrics.complexity_score:.2f}")
    print(f"Token Estimate: {result.metrics.token_estimate}")
    print(f"Quality Score: {result.metrics.quality_score:.2f}")
    
    print("\nImprovement Suggestions:")
    for suggestion in result.metrics.improvement_suggestions:
        print(f"- {suggestion}")
    
    print("\nStructure Analysis:")
    for component, lines in result.structure_analysis.items():
        print(f"\n{component}:")
        for line in lines:
            print(f"  {line}")
    
    print("\nPattern Analysis:")
    for pattern_type, patterns in result.pattern_analysis.items():
        print(f"\n{pattern_type}:")
        for pattern in patterns:
            print(f"  - {pattern}")
    
    print("\nQuality Analysis:")
    for metric, score in result.quality_analysis.items():
        print(f"{metric}: {score:.2f}")

if __name__ == "__main__":
    asyncio.run(main()) 