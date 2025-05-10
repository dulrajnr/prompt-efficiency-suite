"""
Example usage of the CICDIntegration class.
"""

from pathlib import Path

from prompt_efficiency_suite import CICDIntegration


def main():
    # Initialize CI/CD integration with configuration
    config_path = Path("examples/cicd_config.json")
    cicd = CICDIntegration(config_path)

    # Run tests
    print("Running tests...")
    test_result = cicd.run_tests()

    print("\nTest Results:")
    print(f"Passed: {test_result.passed}")
    print(f"Total Tests: {test_result.total_tests}")
    print(f"Passed Tests: {test_result.passed_tests}")
    print(f"Failed Tests: {len(test_result.failed_tests)}")
    print(f"Coverage: {test_result.coverage:.2f}%")
    print(f"Duration: {test_result.duration:.2f} seconds")

    if test_result.failed_tests:
        print("\nFailed Tests:")
        for test in test_result.failed_tests:
            print(f"- {test}")

    # Generate test report
    print("\nGenerating test report...")
    cicd.generate_report("test_report.json")

    # Deploy if tests passed
    if test_result.passed and test_result.coverage >= 80.0:
        print("\nDeploying to PyPI...")
        try:
            deployment_result = cicd.deploy("0.1.0", "pypi")
            print("\nDeployment Results:")
            print(f"Success: {deployment_result.success}")
            print(f"Version: {deployment_result.version}")
            print(f"Timestamp: {deployment_result.timestamp}")
            print("\nArtifacts:")
            for artifact in deployment_result.artifacts:
                print(f"- {artifact}")
            print("\nLogs:")
            for log in deployment_result.logs:
                print(f"- {log}")
        except Exception as e:
            print(f"\nDeployment failed: {e}")
    else:
        print("\nSkipping deployment due to test failures or insufficient coverage")

    # Generate final report
    print("\nGenerating final report...")
    cicd.generate_report("cicd_report.json")

    # Print history
    print("\nTest History:")
    for i, result in enumerate(cicd.get_test_history(), 1):
        print(f"\nRun {i}:")
        print(f"Passed: {result.passed}")
        print(f"Coverage: {result.coverage:.2f}%")
        print(f"Duration: {result.duration:.2f} seconds")

    print("\nDeployment History:")
    for i, result in enumerate(cicd.get_deployment_history(), 1):
        print(f"\nDeployment {i}:")
        print(f"Success: {result.success}")
        print(f"Version: {result.version}")
        print(f"Timestamp: {result.timestamp}")


if __name__ == "__main__":
    main()
