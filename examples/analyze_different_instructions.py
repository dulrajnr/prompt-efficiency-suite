#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different instructions.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, instruction_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {instruction_type} Instruction Prompt:")
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
    
    # Example prompts with different instructions
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
        Make sure to consider all the details.
        Follow these specific steps.
        Pay attention to these important points.
        Example: Here's a detailed example.
        """,
        
        "Step-by-Step": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Step 1: First, do this.
        Step 2: Then, do that.
        Step 3: Finally, do this.
        Example: Here's a step-by-step example.
        """,
        
        "Conditional": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        If condition A is true, do X.
        If condition B is true, do Y.
        Otherwise, do Z.
        Example: Here's a conditional example.
        """,
        
        "Iterative": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Repeat these steps until done.
        Check the results after each iteration.
        Make adjustments as needed.
        Example: Here's an iterative example.
        """,
        
        "Recursive": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Break it down into smaller tasks.
        Solve each sub-task recursively.
        Combine the results.
        Example: Here's a recursive example.
        """
    }
    
    # Analyze each prompt
    for instruction_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, instruction_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 