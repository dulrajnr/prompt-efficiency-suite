import pytest

from prompt_efficiency_suite.analyzer import AnalysisMetrics, AnalysisResult, PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType


@pytest.fixture
def analyzer():
    return PromptAnalyzer()


def test_initialization(analyzer):
    """Test that the analyzer initializes correctly."""
    assert analyzer.clarity_indicators
    assert analyzer.structure_patterns
    assert analyzer.complexity_levels


def test_analyze_prompt(analyzer):
    """Test basic prompt analysis."""
    prompt = """
    System: You are a helpful assistant.
    Context: This is some background information.
    Instruction: Please help me with this task.
    """

    result = analyzer.analyze_prompt(prompt=prompt, model=ModelType.GPT4)

    assert isinstance(result, AnalysisResult)
    assert result.prompt == prompt
    assert isinstance(result.metrics.clarity_score, float)
    assert isinstance(result.metrics.structure_score, float)
    assert isinstance(result.metrics.complexity_score, float)
    assert isinstance(result.metrics.token_estimate, int)
    assert isinstance(result.metrics.quality_score, float)
    assert isinstance(result.metrics.improvement_suggestions, list)
    assert isinstance(result.structure_analysis, dict)
    assert isinstance(result.pattern_analysis, dict)
    assert isinstance(result.quality_analysis, dict)


def test_analyze_prompt_with_target_complexity(analyzer):
    """Test prompt analysis with target complexity."""
    prompt = """
    System: You are a helpful assistant.
    Context: This is some background information.
    Instruction: Please help me with this task.
    """

    result = analyzer.analyze_prompt(prompt=prompt, model=ModelType.GPT4, target_complexity="medium")

    assert isinstance(result, AnalysisResult)
    assert result.metrics.complexity_level in ["low", "medium", "high", "very_high"]


def test_calculate_clarity_score(analyzer):
    """Test clarity score calculation."""
    # Good clarity
    good_prompt = "Please clearly explain the steps to solve this problem."
    score = analyzer._calculate_clarity_score(good_prompt)
    assert score > 0.7

    # Poor clarity
    poor_prompt = "Maybe you could do something about this, etc."
    score = analyzer._calculate_clarity_score(poor_prompt)
    assert score < 0.7


def test_calculate_specificity_score(analyzer):
    """Test specificity score calculation."""
    # Good specificity
    good_prompt = "Please provide 3 examples of how to solve this problem."
    score = analyzer._calculate_specificity_score(good_prompt)
    assert score > 0.7

    # Poor specificity
    poor_prompt = "Do something about this."
    score = analyzer._calculate_specificity_score(poor_prompt)
    assert score < 0.7


def test_calculate_structure_score(analyzer):
    """Test structure score calculation."""
    # Good structure
    good_prompt = """
    System: You are a helpful assistant.
    Context: Some background.
    Instruction: Do something.
    """
    score = analyzer._calculate_structure_score(good_prompt)
    assert score > 0.7

    # Poor structure
    poor_prompt = "help me with this"
    score = analyzer._calculate_structure_score(poor_prompt)
    assert score < 0.7


def test_calculate_context_score(analyzer):
    """Test context score calculation."""
    # Good context
    good_prompt = "Context: This is relevant background information within the scope of the task."
    score = analyzer._calculate_context_score(good_prompt)
    assert score > 0.7

    # Poor context
    poor_prompt = "Do this task."
    score = analyzer._calculate_context_score(poor_prompt)
    assert score < 0.7


def test_calculate_instruction_score(analyzer):
    """Test instruction score calculation."""
    # Good instructions
    good_prompt = "Instruction: Please perform this task and format the output as requested."
    score = analyzer._calculate_instruction_score(good_prompt)
    assert score > 0.7

    # Poor instructions
    poor_prompt = "Do something."
    score = analyzer._calculate_instruction_score(poor_prompt)
    assert score < 0.7


def test_calculate_overall_score(analyzer):
    """Test overall score calculation."""
    metrics = AnalysisMetrics(
        clarity_score=0.8,
        specificity_score=0.7,
        structure_score=0.9,
        context_score=0.6,
        instruction_score=0.8,
        overall_score=0.0,
        token_count=100,
        estimated_cost=0.1,
        complexity_level="medium",
    )

    score = analyzer._calculate_overall_score(metrics)
    assert score >= 0.0
    assert score <= 1.0


def test_determine_complexity_level(analyzer):
    """Test complexity level determination."""
    # Low complexity
    low_prompt = "Do this simple task."
    level = analyzer._determine_complexity_level(low_prompt)
    assert level == "low"

    # Medium complexity
    medium_prompt = """
    System: You are a helpful assistant.
    Context: Some background.
    Instruction: Do something.
    """
    level = analyzer._determine_complexity_level(medium_prompt)
    assert level == "medium"

    # High complexity
    high_prompt = """
    System: You are a helpful assistant.
    Context: This is some detailed background information.
    Instruction: Please perform this complex task.
    Example: Here is an example of what we want.
    Constraint: These are the limitations.
    Format: This is how the output should look.
    """
    level = analyzer._determine_complexity_level(high_prompt)
    assert level in ["high", "very_high"]


def test_get_suggestions(analyzer):
    """Test getting improvement suggestions."""
    prompt = "Do something about this."
    metrics = AnalysisMetrics(
        clarity_score=0.5,
        specificity_score=0.4,
        structure_score=0.3,
        context_score=0.4,
        instruction_score=0.5,
        overall_score=0.4,
        token_count=5,
        estimated_cost=0.001,
        complexity_level="low",
    )

    suggestions = analyzer._get_suggestions(prompt, metrics, "medium")
    assert len(suggestions) > 0
    assert any("clarity" in s.lower() for s in suggestions)
    assert any("specificity" in s.lower() for s in suggestions)
    assert any("structure" in s.lower() for s in suggestions)


def test_identify_strengths(analyzer):
    """Test strength identification."""
    metrics = AnalysisMetrics(
        clarity_score=0.9,
        specificity_score=0.8,
        structure_score=0.7,
        context_score=0.6,
        instruction_score=0.5,
        overall_score=0.7,
        token_count=100,
        estimated_cost=0.1,
        complexity_level="medium",
    )

    strengths = analyzer._identify_strengths(metrics)
    assert len(strengths) > 0
    assert any("clarity" in s.lower() for s in strengths)
    assert any("specificity" in s.lower() for s in strengths)


def test_identify_weaknesses(analyzer):
    """Test weakness identification."""
    metrics = AnalysisMetrics(
        clarity_score=0.5,
        specificity_score=0.4,
        structure_score=0.3,
        context_score=0.4,
        instruction_score=0.5,
        overall_score=0.4,
        token_count=100,
        estimated_cost=0.1,
        complexity_level="medium",
    )

    weaknesses = analyzer._identify_weaknesses(metrics)
    assert len(weaknesses) > 0
    assert any("clarity" in s.lower() for s in weaknesses)
    assert any("specificity" in s.lower() for s in weaknesses)
    assert any("structure" in s.lower() for s in weaknesses)


def test_clarity_score_calculation(analyzer):
    """Test clarity score calculation."""
    # High clarity prompt
    high_clarity = "Please clearly explain how to solve this problem step by step."
    high_score = analyzer._calculate_clarity_score(high_clarity)
    assert high_score > 0.7

    # Low clarity prompt
    low_clarity = "This is really very important and in order to achieve the goal."
    low_score = analyzer._calculate_clarity_score(low_clarity)
    assert low_score < 0.5


def test_structure_score_calculation(analyzer):
    """Test structure score calculation."""
    # Well-structured prompt
    good_structure = """
    System: You are a helpful assistant.
    Context: Some background.
    Instruction: Do something.
    """
    good_score = analyzer._calculate_structure_score(good_structure)
    assert good_score > 0.7

    # Poorly structured prompt
    bad_structure = "help me with this"
    bad_score = analyzer._calculate_structure_score(bad_structure)
    assert bad_score < 0.3


def test_complexity_score_calculation(analyzer):
    """Test complexity score calculation."""
    # Complex prompt
    complex_prompt = "This is a complex and sophisticated task that requires advanced expertise."
    complex_score = analyzer._calculate_complexity_score(complex_prompt)
    assert complex_score > 0.7

    # Simple prompt
    simple_prompt = "This is a simple and straightforward task for beginners."
    simple_score = analyzer._calculate_complexity_score(simple_prompt)
    assert simple_score < 0.3


def test_quality_score_calculation(analyzer):
    """Test quality score calculation."""
    # High quality prompt
    good_prompt = """
    System: You are a helpful assistant.
    Context: This is some background information.
    Instruction: Please help me with this task step by step.
    """
    good_score = analyzer._calculate_quality_score(good_prompt)
    assert good_score > 0.7

    # Low quality prompt
    bad_prompt = "help me"
    bad_score = analyzer._calculate_quality_score(bad_prompt)
    assert bad_score < 0.5


def test_suggestion_generation(analyzer):
    """Test improvement suggestion generation."""
    # Prompt needing clarity
    clarity_prompt = "This is really very important and in order to achieve the goal."
    clarity_suggestions = analyzer._generate_suggestions(
        clarity_prompt, clarity_score=0.3, structure_score=0.5, complexity_score=0.5
    )
    assert any("clarity" in s.lower() for s in clarity_suggestions)

    # Prompt needing structure
    structure_prompt = "help me with this task"
    structure_suggestions = analyzer._generate_suggestions(
        structure_prompt, clarity_score=0.5, structure_score=0.3, complexity_score=0.5
    )
    assert any("structure" in s.lower() for s in structure_suggestions)

    # Prompt needing complexity adjustment
    complex_prompt = "This is a complex and sophisticated task."
    complex_suggestions = analyzer._generate_suggestions(
        complex_prompt, clarity_score=0.5, structure_score=0.5, complexity_score=0.9
    )
    assert any("simplify" in s.lower() for s in complex_suggestions)


def test_structure_analysis(analyzer):
    """Test structure analysis."""
    prompt = """
    System: You are a helpful assistant.
    Context: Some background.
    Instruction: Do something.
    Example: Here's how.
    """

    analysis = analyzer._analyze_structure(prompt)

    assert "system_prompt" in analysis
    assert "context_block" in analysis
    assert "instruction_block" in analysis
    assert "example_block" in analysis
    assert len(analysis["system_prompt"]) == 1
    assert len(analysis["context_block"]) == 1
    assert len(analysis["instruction_block"]) == 1
    assert len(analysis["example_block"]) == 1


def test_pattern_analysis(analyzer):
    """Test pattern analysis."""
    prompt = """
    This is really very important.
    Please clearly explain this complex task.
    """

    analysis = analyzer._analyze_patterns(prompt)

    assert "clarity_patterns" in analysis
    assert "complexity_patterns" in analysis
    assert "redundant_patterns" in analysis
    assert len(analysis["clarity_patterns"]) > 0
    assert len(analysis["complexity_patterns"]) > 0
    assert len(analysis["redundant_patterns"]) > 0


def test_quality_analysis(analyzer):
    """Test quality analysis."""
    prompt = """
    System: You are a helpful assistant.
    Context: This is some background information.
    Instruction: Please help me with this task step by step.
    """

    analysis = analyzer._analyze_quality(prompt)

    assert "clarity" in analysis
    assert "structure" in analysis
    assert "complexity" in analysis
    assert "overall" in analysis
    assert all(0 <= score <= 1 for score in analysis.values())


def test_token_estimation(analyzer):
    """Test token estimation."""
    prompt = "This is a test prompt with multiple words."
    tokens = analyzer._estimate_tokens(prompt)
    assert tokens > 0
    assert tokens == len(prompt.split())


def test_metadata_handling(analyzer):
    """Test metadata handling in analysis."""
    metadata = {"key": "value", "number": 42}

    result = analyzer.analyze_prompt(prompt="Test prompt", model=ModelType.GPT4, metadata=metadata)

    assert result.metadata == metadata


def test_model_specific_analysis(analyzer):
    """Test model-specific analysis."""
    # Test with different models
    for model in ModelType:
        result = analyzer.analyze_prompt(prompt="Test prompt", model=model)

        assert isinstance(result, AnalysisResult)
        assert result.metrics.quality_score >= 0
        assert result.metrics.quality_score <= 1
