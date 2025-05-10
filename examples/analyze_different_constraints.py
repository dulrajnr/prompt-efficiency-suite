#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different constraints.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, constraint_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {constraint_type} Constraint Prompt:")
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

    # Example prompts with different constraints
    prompts = {
        "None": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "Simple": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        """,
        "Multiple": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        It should be scalable and maintainable.
        It needs to handle edge cases properly.
        """,
        "Technical": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        It should be scalable and maintainable.
        It needs to handle edge cases properly.
        It must follow best practices.
        It should be well-documented.
        It needs to be tested thoroughly.
        """,
        "Business": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be cost-effective.
        It should be marketable and profitable.
        It needs to meet customer requirements.
        It must comply with regulations.
        It should be sustainable.
        It needs to be scalable.
        """,
        "Complex": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        It should be scalable and maintainable.
        It needs to handle edge cases properly.
        It must follow best practices.
        It should be well-documented.
        It needs to be tested thoroughly.
        It must be cost-effective.
        It should be marketable and profitable.
        It needs to meet customer requirements.
        It must comply with regulations.
        It should be sustainable.
        It needs to be scalable.
        """,
    }

    # Analyze each prompt
    for constraint_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, constraint_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
