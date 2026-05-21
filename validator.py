from rules import ACADEMIC_RULES
from syllabus_reader import extract_syllabus_info


def validate_syllabus(file_path, rule_name,info):

    info = extract_syllabus_info(file_path)

    rule = ACADEMIC_RULES[rule_name]

    results = []
    results.append(
        f"✓ Course: "
        f"{info.get('course_code')} - "
        f"{info.get('course_title')}"
    )

    results.append(
    f"✓ Detected Type: {rule_name}"
    )

    # -------------------------------------------------
    # SECTIONS
    # -------------------------------------------------
    checks = [

        ("Course Summary",
         info["has_course_summary"]),

        ("Course Outcomes",
         info["has_course_outcomes"]),

        ("Detailed Syllabus",
         info["has_detailed_syllabus"]),

        ("References",
         info["has_references"])
    ]

    for name, status in checks:

        if status:
            results.append(f"✓ {name} found")
        else:
            results.append(f"✗ {name} missing")

    # -------------------------------------------------
    # COURSE OUTCOMES
    # -------------------------------------------------
    co_count = info["co_count"]

    if co_count > 0:
        results.append(
            f"✓ Course Outcomes detected ({co_count})"
        )
    else:
        results.append(
            "✗ Course Outcomes missing"
        )

       # -------------------------------------------------
    # RULE-BASED VALUES
    # -------------------------------------------------

    results.append(
        f"✓ Credits as per rule: "
        f"{rule['credits']}"
    )

    results.append(
        f"✓ Hours/week as per rule: "
        f"{rule['hours_per_week']}"
    )
    return results
