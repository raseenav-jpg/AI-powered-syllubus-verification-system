def calculate_similarity(results):

    passed = 0
    failed = 0

    # FULL SYLLABUS
    if results and isinstance(results[0], dict):

        for course in results:

            for line in course["validation_results"]:

                if line.startswith("✓"):
                    passed += 1
                else:
                    failed += 1

    # SINGLE COURSE
    else:

        for line in results:

            if line.startswith("✓"):
                passed += 1
            else:
                failed += 1

    total = passed + failed

    score = (
        round((passed / total) * 100, 2)
        if total > 0 else 0
    )

    decision = (
        "PASS"
        if score >= 70
        else "REVIEW REQUIRED"
    )

    return {
        "passed": passed,
        "failed": failed,
        "score": score,
        "decision": decision
    }
