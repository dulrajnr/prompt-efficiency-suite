#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different tones.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, tone_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {tone_type} Tone Prompt:")
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

    # Example prompts with different tones
    prompts = {
        "Formal": """
        System: You are a professional assistant.
        Context: This is the background information.
        Instruction: Please provide assistance with the following task.
        Example: Here is an example of the expected output.
        """,
        "Casual": """
        System: You're a friendly helper.
        Context: Here's what's going on...
        Instruction: Can you help me with this?
        Example: Here's what I'm looking for.
        """,
        "Technical": """
        System: You are a technical assistant.
        Context: The following parameters and constraints apply.
        Instruction: Implement the specified functionality.
        Example: See the following code snippet.
        """,
        "Friendly": """
        System: You're a helpful friend.
        Context: I'm working on something cool.
        Instruction: Mind giving me a hand with this?
        Example: Here's what I'm trying to do.
        """,
        "Professional": """
        System: You are a professional consultant.
        Context: This is a business requirement.
        Instruction: Please provide a detailed analysis.
        Example: Here's a similar case study.
        """,
        "Conversational": """
        System: You're a chatty assistant.
        Context: So here's the deal...
        Instruction: What do you think about this?
        Example: Here's what I'm thinking...
        """,
    }

    # Analyze each prompt
    for tone_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, tone_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
