#!/usr/bin/env python3
"""
Example script demonstrating analysis of different types of prompts.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, description):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {description}:")
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
    
    # Example prompts
    prompts = {
        "Well-Structured Prompt": """
        System: You are a helpful assistant.
        Context: This is some background information about the task.
        Instruction: Please help me with this task step by step.
        Example: Here's how to do it.
        """,
        
        "Unclear Prompt": """
        This is really very important and in order to achieve the goal we need to
        make sure that everything is properly done and all the necessary steps
        are taken into consideration.
        """,
        
        "Complex Prompt": """
        Given the intricate nature of quantum mechanics and its implications on
        string theory, please provide a comprehensive analysis of how these
        concepts relate to general relativity, taking into account the various
        mathematical frameworks and theoretical models that have been proposed.
        """,
        
        "Simple Prompt": """
        Help me write a function to add two numbers.
        """,
        
        "Redundant Prompt": """
        Please help me with this task. I really need help with this task.
        This task is very important. I need to complete this task.
        Can you help me with this task?
        """,
        
        "Technical Prompt": """
        Implement a REST API endpoint that handles CRUD operations for a user
        management system, including authentication, authorization, and data
        validation, while following best practices for security and performance.
        """
    }
    
    # Analyze each prompt
    for description, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, description)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 