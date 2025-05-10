#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different contexts.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, context_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {context_type} Context Prompt:")
    print("=" * 50)
    print(f"Prompt:\n{prompt}")

    result = analyzer.analyze_prompt(prompt=prompt, model=ModelType.GPT4)

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

    # Example prompts with different contexts
    prompts = {
        "Simple": """
        System: You are a helpful assistant.
        Context: This is a simple task.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "Complex": """
        System: You are a helpful assistant.
        Context: This is a complex task with multiple aspects.
        It involves several steps and considerations.
        There are many factors to take into account.
        Instruction: Help me with this complex task.
        Example: Here's a complex example.
        """,
        "Technical": """
        System: You are a helpful assistant.
        Context: This is a technical task.
        It involves programming and system design.
        There are specific requirements and constraints.
        Instruction: Help me with this technical task.
        Example: Here's a technical example.
        """,
        "Business": """
        System: You are a helpful assistant.
        Context: This is a business task.
        It involves market analysis and strategy.
        There are financial and operational considerations.
        Instruction: Help me with this business task.
        Example: Here's a business example.
        """,
        "Academic": """
        System: You are a helpful assistant.
        Context: This is an academic task.
        It involves research and analysis.
        There are theoretical and practical aspects.
        Instruction: Help me with this academic task.
        Example: Here's an academic example.
        """,
        "Creative": """
        System: You are a helpful assistant.
        Context: This is a creative task.
        It involves imagination and innovation.
        There are artistic and expressive elements.
        Instruction: Help me with this creative task.
        Example: Here's a creative example.
        """,
    }

    # Analyze each prompt
    for context_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, context_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
