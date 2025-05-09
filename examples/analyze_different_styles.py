#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different styles.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, style_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {style_type} Style Prompt:")
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
    
    # Example prompts with different styles
    prompts = {
        "Direct": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        
        "Narrative": """
        System: You are a helpful assistant.
        Context: Once upon a time, there was a task that needed to be done.
        The background information was complex and required careful consideration.
        Instruction: Help me navigate through this task and find a solution.
        Example: Here's a story of how it was done before.
        """,
        
        "Question-Based": """
        System: You are a helpful assistant.
        Context: What is the background information?
        Instruction: How can you help me with this task?
        Example: What does a good example look like?
        """,
        
        "Step-by-Step": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Let's solve this task step by step.
        Step 1: First, understand the context.
        Step 2: Then, follow the instructions.
        Step 3: Finally, check the example.
        Example: Here's how to do it step by step.
        """,
        
        "Problem-Solution": """
        System: You are a helpful assistant.
        Context: This is the problem we need to solve.
        Instruction: Let's find a solution to this problem.
        Example: Here's how a similar problem was solved.
        """,
        
        "Compare-Contrast": """
        System: You are a helpful assistant.
        Context: Here are two different approaches.
        Instruction: Compare and contrast these approaches.
        Example: Here's how they differ in practice.
        """
    }
    
    # Analyze each prompt
    for style_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, style_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 