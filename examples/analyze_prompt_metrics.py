#!/usr/bin/env python3
"""
Example script demonstrating prompt analysis with different metrics and evaluation criteria.
"""

from prompt_efficiency_suite import PromptAnalyzer


def analyze_prompt_metrics():
    """Analyze prompts with different metrics and evaluation criteria."""
    analyzer = PromptAnalyzer()

    # Example 1: Analyzing a prompt with clarity metrics
    prompt1 = """
    Create a function that takes a list of numbers and returns the sum of all even numbers.
    The function should handle empty lists and invalid inputs gracefully.
    """

    print("\n=== Example 1: Clarity Metrics ===")
    print("\nPrompt:")
    print(prompt1)

    analysis1 = analyzer.analyze_prompt(prompt=prompt1, metrics=["clarity", "specificity", "completeness"])

    print("\nAnalysis:")
    print(f"Clarity Score: {analysis1['clarity_score']}")
    print(f"Specificity Score: {analysis1['specificity_score']}")
    print(f"Completeness Score: {analysis1['completeness_score']}")
    print("\nImprovement Suggestions:")
    for suggestion in analysis1["improvement_suggestions"]:
        print(f"- {suggestion}")

    # Example 2: Analyzing a prompt with structure metrics
    prompt2 = """
    Write a blog post about the benefits of meditation.
    Include an introduction, main points, and conclusion.
    Use a friendly and engaging tone.
    """

    print("\n=== Example 2: Structure Metrics ===")
    print("\nPrompt:")
    print(prompt2)

    analysis2 = analyzer.analyze_prompt(prompt=prompt2, metrics=["structure", "organization", "coherence"])

    print("\nAnalysis:")
    print(f"Structure Score: {analysis2['structure_score']}")
    print(f"Organization Score: {analysis2['organization_score']}")
    print(f"Coherence Score: {analysis2['coherence_score']}")
    print("\nImprovement Suggestions:")
    for suggestion in analysis2["improvement_suggestions"]:
        print(f"- {suggestion}")

    # Example 3: Analyzing a prompt with complexity metrics
    prompt3 = """
    Develop a machine learning model that can predict customer churn based on historical data.
    The model should consider factors such as customer behavior, purchase history, and interaction patterns.
    Include feature engineering, model selection, and evaluation metrics.
    """

    print("\n=== Example 3: Complexity Metrics ===")
    print("\nPrompt:")
    print(prompt3)

    analysis3 = analyzer.analyze_prompt(prompt=prompt3, metrics=["complexity", "technical_depth", "scope"])

    print("\nAnalysis:")
    print(f"Complexity Score: {analysis3['complexity_score']}")
    print(f"Technical Depth Score: {analysis3['technical_depth_score']}")
    print(f"Scope Score: {analysis3['scope_score']}")
    print("\nImprovement Suggestions:")
    for suggestion in analysis3["improvement_suggestions"]:
        print(f"- {suggestion}")

    # Example 4: Analyzing a prompt with effectiveness metrics
    prompt4 = """
    Create a marketing campaign for a new product launch.
    The campaign should target young professionals and highlight the product's unique features.
    Include social media strategy, content calendar, and performance metrics.
    """

    print("\n=== Example 4: Effectiveness Metrics ===")
    print("\nPrompt:")
    print(prompt4)

    analysis4 = analyzer.analyze_prompt(prompt=prompt4, metrics=["effectiveness", "impact", "measurability"])

    print("\nAnalysis:")
    print(f"Effectiveness Score: {analysis4['effectiveness_score']}")
    print(f"Impact Score: {analysis4['impact_score']}")
    print(f"Measurability Score: {analysis4['measurability_score']}")
    print("\nImprovement Suggestions:")
    for suggestion in analysis4["improvement_suggestions"]:
        print(f"- {suggestion}")


if __name__ == "__main__":
    analyze_prompt_metrics()
