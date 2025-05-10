private fun createTeamAnalytics(teamId: String): TeamAnalytics {
    val teamPatterns = teamPatterns[teamId] ?: emptyList()
    val teamMembers = teamMembers.values.filter { it.teamId == teamId }

    // Calculate total cost and usage
    val totalCost = teamPatterns.sumOf { it.averageCost * it.usageCount }
    val costByMember = teamMembers.associate { member ->
        member.id to teamPatterns
            .filter { it.createdBy == member.id }
            .sumOf { it.averageCost * it.usageCount }
    }

    val costByPattern = teamPatterns.associate { pattern ->
        pattern.id to (pattern.averageCost * pattern.usageCount)
    }

    val usageByMember = teamMembers.associate { member ->
        member.id to teamPatterns
            .filter { it.createdBy == member.id }
            .sumOf { it.usageCount }
    }

    val usageByPattern = teamPatterns.associate { pattern ->
        pattern.id to pattern.usageCount
    }

    // Generate best practices
    val bestPractices = generateBestPractices(teamPatterns)

    // Generate trends
    val trends = generateTrends(teamPatterns)

    return TeamAnalytics(
        teamId = teamId,
        totalCost = totalCost,
        costByMember = costByMember,
        costByPattern = costByPattern,
        usageByMember = usageByMember,
        usageByPattern = usageByPattern,
        bestPractices = bestPractices,
        trends = trends
    )
}

private fun updatePatternAnalytics(pattern: TeamPattern) {
    val teamPatterns = teamPatterns[pattern.teamId] ?: mutableListOf()
    val existingPattern = teamPatterns.find { it.id == pattern.id }

    if (existingPattern != null) {
        // Update existing pattern
        val updatedPattern = existingPattern.copy(
            usageCount = pattern.usageCount,
            averageCost = pattern.averageCost,
            lastModifiedAt = LocalDateTime.now()
        )
        teamPatterns[teamPatterns.indexOf(existingPattern)] = updatedPattern
    } else {
        // Add new pattern
        teamPatterns.add(pattern)
    }

    // Update team analytics
    teamAnalytics[pattern.teamId] = createTeamAnalytics(pattern.teamId)
}

private fun generateBestPractices(patterns: List<TeamPattern>): List<BestPractice> {
    val bestPractices = mutableListOf<BestPractice>()

    // Analyze pattern success rates
    val highSuccessPatterns = patterns.filter { it.successRate >= 0.8 }
    if (highSuccessPatterns.isNotEmpty()) {
        bestPractices.add(BestPractice(
            title = "High Success Rate Patterns",
            description = "The following patterns have shown high success rates:",
            patterns = highSuccessPatterns.map { it.name }
        ))
    }

    // Analyze cost efficiency
    val costEfficientPatterns = patterns.filter { it.averageCost <= 0.01 }
    if (costEfficientPatterns.isNotEmpty()) {
        bestPractices.add(BestPractice(
            title = "Cost-Efficient Patterns",
            description = "These patterns provide good value for their cost:",
            patterns = costEfficientPatterns.map { it.name }
        ))
    }

    // Analyze usage patterns
    val popularPatterns = patterns.sortedByDescending { it.usageCount }.take(3)
    if (popularPatterns.isNotEmpty()) {
        bestPractices.add(BestPractice(
            title = "Most Used Patterns",
            description = "These patterns are most frequently used by the team:",
            patterns = popularPatterns.map { it.name }
        ))
    }

    return bestPractices
}

private fun generateTrends(patterns: List<TeamPattern>): List<TeamTrend> {
    val trends = mutableListOf<TeamTrend>()

    // Analyze usage growth
    val usageGrowth = patterns
        .groupBy { it.createdAt.toLocalDate() }
        .mapValues { it.value.sumOf { pattern -> pattern.usageCount } }
        .toSortedMap()

    if (usageGrowth.size >= 2) {
        val growthRate = calculateGrowthRate(usageGrowth.values.toList())
        trends.add(TeamTrend(
            type = TrendType.USAGE_GROWTH,
            value = growthRate,
            description = "Pattern usage is ${if (growthRate > 0) "increasing" else "decreasing"} by ${abs(growthRate)}%"
        ))
    }

    // Analyze cost trends
    val costTrends = patterns
        .groupBy { it.createdAt.toLocalDate() }
        .mapValues { it.value.sumOf { pattern -> pattern.averageCost * pattern.usageCount } }
        .toSortedMap()

    if (costTrends.size >= 2) {
        val costChange = calculateGrowthRate(costTrends.values.toList())
        trends.add(TeamTrend(
            type = TrendType.COST_TREND,
            value = costChange,
            description = "Pattern costs are ${if (costChange > 0) "increasing" else "decreasing"} by ${abs(costChange)}%"
        ))
    }

    // Analyze success rate trends
    val successTrends = patterns
        .groupBy { it.createdAt.toLocalDate() }
        .mapValues { it.value.map { pattern -> pattern.successRate }.average() }
        .toSortedMap()

    if (successTrends.size >= 2) {
        val successChange = calculateGrowthRate(successTrends.values.toList())
        trends.add(TeamTrend(
            type = TrendType.SUCCESS_RATE,
            value = successChange,
            description = "Pattern success rates are ${if (successChange > 0) "improving" else "declining"} by ${abs(successChange)}%"
        ))
    }

    return trends
}

private fun calculateGrowthRate(values: List<Double>): Double {
    if (values.size < 2) return 0.0
    val firstValue = values.first()
    val lastValue = values.last()
    return ((lastValue - firstValue) / firstValue) * 100
}

data class BestPractice(
    val title: String,
    val description: String,
    val patterns: List<String>
)

data class TeamTrend(
    val type: TrendType,
    val value: Double,
    val description: String
)

enum class TrendType {
    USAGE_GROWTH,
    COST_TREND,
    SUCCESS_RATE
}
