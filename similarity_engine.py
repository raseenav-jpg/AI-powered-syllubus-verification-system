def calculate_similarity(results):
    """
    Calculate similarity score based on the number of passed and failed checks.
    A result starting with '✓' is considered a pass.
    A result starting with '✗' is considered a fail.
    """

    total_checks = len(results)

    if total_checks == 0:
        return {
            "passed": 0,
            "failed": 0,
            "score": 0.0,
            "decision": "No Checks Performed"
        }

    passed = sum(1 for r in results if r.startswith("✓"))
    failed = total_checks - passed

    score = (passed / total_checks) * 100

    # Final decision rules
    if score >= 95:
        decision = "Approved"
    elif score >= 80:
        decision = "Minor Corrections Needed"
    else:
        decision = "Major Corrections Needed"

    return {
        "passed": passed,
        "failed": failed,
        "score": round(score, 2),
        "decision": decision
    }
