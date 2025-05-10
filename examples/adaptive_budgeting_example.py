"""
Example usage of the AdaptiveBudgeting class.
"""

import time
from datetime import datetime, timedelta
from pathlib import Path

from prompt_efficiency_suite import AdaptiveBudgeting


def main():
    # Initialize budget management with configuration
    config_path = Path("examples/budget_config.json")
    budgeting = AdaptiveBudgeting(config_path)

    # Simulate some API requests
    print("Simulating API requests...")

    # GPT-4 requests
    print("\nGPT-4 Requests:")
    for i in range(5):
        tokens = 1000 * (i + 1)
        cost = 0.1 * (i + 1)
        budgeting.update_metrics("gpt-4", tokens, cost)
        print(f"Request {i + 1}: {tokens} tokens, ${cost:.2f}")
        time.sleep(1)  # Simulate request delay

    # GPT-3.5-Turbo requests
    print("\nGPT-3.5-Turbo Requests:")
    for i in range(3):
        tokens = 2000 * (i + 1)
        cost = 0.05 * (i + 1)
        budgeting.update_metrics("gpt-3.5-turbo", tokens, cost)
        print(f"Request {i + 1}: {tokens} tokens, ${cost:.2f}")
        time.sleep(1)  # Simulate request delay

    # Get and print metrics
    print("\nBudget Metrics:")
    for model in ["gpt-4", "gpt-3.5-turbo"]:
        metrics = budgeting.get_metrics(model)
        print(f"\n{model}:")
        print(f"Total Tokens: {metrics.total_tokens:,}")
        print(f"Total Cost: ${metrics.total_cost:.2f}")
        print(f"Average Tokens/Request: {metrics.average_tokens_per_request:.1f}")
        print(f"Average Cost/Request: ${metrics.average_cost_per_request:.2f}")
        print(f"Peak Tokens: {metrics.peak_tokens:,}")
        print(f"Peak Cost: ${metrics.peak_cost:.2f}")
        print(f"Request Count: {metrics.request_count}")

    # Get and print alerts
    print("\nBudget Alerts:")
    alerts = budgeting.get_alerts()
    if alerts:
        for alert in alerts:
            print(f"\nAlert at {alert.timestamp}:")
            print(f"Type: {alert.alert_type}")
            print(f"Message: {alert.message}")
            print(f"Threshold: {alert.threshold}")
            print(f"Current Value: {alert.current_value}")
    else:
        print("No alerts generated")

    # Export metrics and alerts
    print("\nExporting metrics and alerts...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    budgeting.export_metrics(f"metrics_{timestamp}.json")
    budgeting.export_alerts(f"alerts_{timestamp}.json")

    # Get filtered alerts
    print("\nFiltered Alerts:")

    # Get alerts for GPT-4
    gpt4_alerts = budgeting.get_alerts(model="gpt-4")
    print(f"\nGPT-4 Alerts: {len(gpt4_alerts)}")

    # Get alerts by type
    token_alerts = budgeting.get_alerts(alert_type="token_threshold")
    print(f"Token Threshold Alerts: {len(token_alerts)}")

    # Get alerts by time range
    start_time = datetime.now() - timedelta(minutes=5)
    end_time = datetime.now() + timedelta(minutes=5)
    time_alerts = budgeting.get_alerts(start_time=start_time, end_time=end_time)
    print(f"Recent Alerts: {len(time_alerts)}")

    # Reset metrics for a model
    print("\nResetting metrics for GPT-3.5-Turbo...")
    budgeting.reset_metrics("gpt-3.5-turbo")
    metrics = budgeting.get_metrics("gpt-3.5-turbo")
    print(f"New Total Tokens: {metrics.total_tokens}")
    print(f"New Total Cost: ${metrics.total_cost:.2f}")

    # Verify GPT-4 metrics are unchanged
    metrics = budgeting.get_metrics("gpt-4")
    print(f"\nGPT-4 Metrics (unchanged):")
    print(f"Total Tokens: {metrics.total_tokens:,}")
    print(f"Total Cost: ${metrics.total_cost:.2f}")


if __name__ == "__main__":
    main()
