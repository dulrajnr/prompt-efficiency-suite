#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different domains.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, domain_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {domain_type} Domain Prompt:")
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
    
    # Example prompts with different domains
    prompts = {
        "General": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        
        "Technical": """
        System: You are a technical assistant.
        Context: This is a software development task.
        Instruction: Help me implement this feature.
        Example: Here's a code example.
        """,
        
        "Creative": """
        System: You are a creative assistant.
        Context: This is a creative writing task.
        Instruction: Help me write a story.
        Example: Here's a story example.
        """,
        
        "Business": """
        System: You are a business assistant.
        Context: This is a business analysis task.
        Instruction: Help me analyze this market.
        Example: Here's a market analysis example.
        """,
        
        "Educational": """
        System: You are an educational assistant.
        Context: This is a teaching task.
        Instruction: Help me explain this concept.
        Example: Here's a teaching example.
        """,
        
        "Scientific": """
        System: You are a scientific assistant.
        Context: This is a research task.
        Instruction: Help me analyze this data.
        Example: Here's a research example.
        """
    }
    
    # Analyze each prompt
    for domain_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, domain_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 