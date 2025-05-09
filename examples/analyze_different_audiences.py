#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different audiences.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, audience_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {audience_type} Audience Prompt:")
    print("=" * 50)
    print(f"Prompt:\n{prompt}")
    
    result = analyzer.analyze_prompt(
        prompt=prompt,
        model=ModelType.GPT4
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
    
    # Example prompts with different audiences
    prompts = {
        "General": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        
        "Technical": """
        System: You are a technical assistant.
        Context: This is a technical task.
        Instruction: Help me with this technical task.
        Example: Here's a technical example.
        """,
        
        "Business": """
        System: You are a business assistant.
        Context: This is a business task.
        Instruction: Help me with this business task.
        Example: Here's a business example.
        """,
        
        "Academic": """
        System: You are an academic assistant.
        Context: This is an academic task.
        Instruction: Help me with this academic task.
        Example: Here's an academic example.
        """,
        
        "Creative": """
        System: You are a creative assistant.
        Context: This is a creative task.
        Instruction: Help me with this creative task.
        Example: Here's a creative example.
        """,
        
        "Professional": """
        System: You are a professional assistant.
        Context: This is a professional task.
        Instruction: Help me with this professional task.
        Example: Here's a professional example.
        """
    }
    
    # Analyze each prompt
    for audience_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, audience_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 