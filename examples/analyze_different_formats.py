#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different formats.
"""

import asyncio

from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


async def analyze_prompt(analyzer, prompt, format_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {format_type} Format Prompt:")
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

    # Example prompts with different formats
    prompts = {
        "Plain Text": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        "Markdown": """
        # System
        You are a helpful assistant.

        ## Context
        This is the background information.

        ## Instruction
        Help me with this task.

        ## Example
        Here's an example.
        """,
        "JSON": """
        {
            "system": "You are a helpful assistant.",
            "context": "This is the background information.",
            "instruction": "Help me with this task.",
            "example": "Here's an example."
        }
        """,
        "YAML": """
        system: You are a helpful assistant.
        context: This is the background information.
        instruction: Help me with this task.
        example: Here's an example.
        """,
        "XML": """
        <prompt>
            <system>You are a helpful assistant.</system>
            <context>This is the background information.</context>
            <instruction>Help me with this task.</instruction>
            <example>Here's an example.</example>
        </prompt>
        """,
        "HTML": """
        <div class="prompt">
            <div class="system">You are a helpful assistant.</div>
            <div class="context">This is the background information.</div>
            <div class="instruction">Help me with this task.</div>
            <div class="example">Here's an example.</div>
        </div>
        """,
    }

    # Analyze each prompt
    for format_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, format_type)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
