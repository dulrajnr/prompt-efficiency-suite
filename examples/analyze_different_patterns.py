#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different patterns.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, pattern_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {pattern_type} Pattern Prompt:")
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
    
    # Example prompts with different patterns
    prompts = {
        "Basic": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        
        "Chain of Thought": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Let's think about this step by step.
        First, we need to understand the problem.
        Then, we can identify the key components.
        Finally, we can develop a solution.
        Example: Here's an example of the thought process.
        """,
        
        "Few Shot": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example 1: Here's the first example.
        Example 2: Here's the second example.
        Example 3: Here's the third example.
        """,
        
        "Zero Shot": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        """,
        
        "Role Play": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Role: You are an expert in this field.
        Example: Here's an example of the role play.
        """,
        
        "Hybrid": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Let's think about this step by step.
        First, we need to understand the problem.
        Then, we can identify the key components.
        Finally, we can develop a solution.
        Example 1: Here's the first example.
        Example 2: Here's the second example.
        Example 3: Here's the third example.
        Role: You are an expert in this field.
        """
    }
    
    # Analyze each prompt
    for pattern_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, pattern_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 