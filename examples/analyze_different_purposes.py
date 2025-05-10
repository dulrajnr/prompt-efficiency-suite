#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different purposes.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, purpose_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {purpose_type} Purpose Prompt:")
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

    # Example prompts with different purposes
    prompts = {
        "Informative": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me understand this topic.
        Example: Here's an example explanation.
        """,
        "Instructional": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me learn how to do this.
        Example: Here's a step-by-step example.
        """,
        "Analytical": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me analyze this situation.
        Example: Here's an analysis example.
        """,
        "Creative": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me create something new.
        Example: Here's a creative example.
        """,
        "Problem-Solving": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me solve this problem.
        Example: Here's a solution example.
        """,
        "Decision-Making": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me make a decision.
        Example: Here's a decision-making example.
        """,
    }

    # Analyze each prompt
    for purpose_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, purpose_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
