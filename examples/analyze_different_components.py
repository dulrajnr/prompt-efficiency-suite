#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different components.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, component_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {component_type} Component:")
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

    # Example prompts with different components
    prompts = {
        "System Only": """
        System: You are a helpful assistant.
        """,
        "System and Instruction": """
        System: You are a helpful assistant.
        Instruction: Help me with this task.
        """,
        "System, Context, and Instruction": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        """,
        "System, Context, Instruction, and Example": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "System, Context, Instruction, Example, and Constraints": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        """,
        "System, Context, Instruction, Example, Constraints, and Notes": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        Notes: Additional considerations and tips.
        """,
    }

    # Analyze each prompt
    for component_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, component_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
