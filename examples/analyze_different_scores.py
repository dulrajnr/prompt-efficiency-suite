#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different scores.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, score_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {score_type} Score Prompt:")
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

    # Example prompts with different scores
    prompts = {
        "Low Clarity": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "High Clarity": """
        System: You are a helpful assistant.
        Context: This is the background information.
        It includes important details and considerations.
        Instruction: Help me with this task.
        Make sure to consider all the details.
        Example: Here's a clear example.
        """,
        "Low Structure": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "High Structure": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        Constraints: The solution must be efficient.
        """,
        "Low Complexity": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "High Complexity": """
        System: You are a helpful assistant.
        Context: This is the background information.
        It includes important details and considerations.
        There are several key points to understand.
        The problem has multiple aspects to consider.
        Instruction: Help me with this task.
        Make sure to consider all the details.
        Follow these specific steps.
        Pay attention to these important points.
        Example: Here's a complex example.
        Constraints: The solution must be efficient.
        It should be scalable and maintainable.
        It needs to handle edge cases properly.
        """,
    }

    # Analyze each prompt
    for score_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, score_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
