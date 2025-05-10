#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different examples.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, example_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {example_type} Example Prompt:")
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

    # Example prompts with different examples
    prompts = {
        "Simple": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "Detailed": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's a detailed example.
        It shows how to do the task step by step.
        It includes all the necessary details.
        It demonstrates the expected outcome.
        """,
        "Multiple": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example 1: Here's the first example.
        Example 2: Here's the second example.
        Example 3: Here's the third example.
        """,
        "Edge Cases": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example 1: Here's a normal case example.
        Example 2: Here's an edge case example.
        Example 3: Here's an error case example.
        """,
        "Step-by-Step": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's a step-by-step example.
        Step 1: First, do this.
        Step 2: Then, do that.
        Step 3: Finally, do this.
        """,
        "Comparative": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example 1: Here's a good example.
        Example 2: Here's a bad example.
        Example 3: Here's a better example.
        """,
    }

    # Analyze each prompt
    for example_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, example_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
