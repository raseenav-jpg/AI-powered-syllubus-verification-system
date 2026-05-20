from rules import ACADEMIC_RULES
from syllabus_reader import extract_syllabus_info


def validate_syllabus(file_path, rule_name):
    """
    Validate a syllabus against the selected academic rule.
    """

    # Extract all information from the syllabus
    info = extract_syllabus_info(file_path)

    # Load the selected rule
    rule = ACADEMIC_RULES[rule_name]

    # Store validation messages
    results = []

    # ---------------------------------------------------------
    # REQUIRED SECTIONS
    # ---------------------------------------------------------
    section_checks = [
        ("Course Summary", info["has_course_summary"]),
        ("Course Outcomes", info["has_course_outcomes"]),
        ("Detailed Syllabus", info["has_detailed_syllabus"]),
        ("Mapped CO", info["has_mapped_co"]),
        ("CO–PO–PSO Mapping", info["has_copo_pso_mapping"]),
        ("Assessment Rubrics", info["has_assessment_rubrics"]),
        ("References", info["has_references"]),
    ]

    for section_name, present in section_checks:
        if present:
            results.append(f"✓ {section_name} found")
        else:
            results.append(f"✗ {section_name} missing")
    # ---------------------------------------------------------
    # COURSE OUTCOMES
    # ---------------------------------------------------------
    co_count = info["co_count"]

    if co_count > 0:
        results.append(
            f"✓ Course Outcomes found ({co_count})"
        )
    else:
        results.append(
            "✗ No Course Outcomes detected"
        )

    # ---------------------------------------------------------
    # HOURS VALIDATION
    # ---------------------------------------------------------
    if (
        info["fixed_hours"] is not None
        and info["open_ended_hours"] is not None
        and info["total_hours"] is not None
    ):
        expected_total = rule["total_hours"]

        # Accept the split written in the syllabus, but ensure
        # that the total matches the selected course rule.
        if info["total_hours"] == expected_total:
            results.append(
                f"✓ Fixed module hours detected ({info['fixed_hours']})"
            )
            results.append(
                f"✓ Open-ended module hours detected "
                f"({info['open_ended_hours']})"
            )
            results.append(
                f"✓ Total hours correct ({info['total_hours']})"
            )
        else:
            results.append(
                f"✗ Total hours incorrect "
                f"(Expected: {expected_total}, "
                f"Found: {info['total_hours']})"
            )
            results.append(
                f"✓ Fixed module hours detected ({info['fixed_hours']})"
            )
            results.append(
                f"✓ Open-ended module hours detected "
                f"({info['open_ended_hours']})"
            )
    else:
        if info.get("hours_error_message"):
            results.append(
                f"✗ {info['hours_error_message']}"
            )
        else:
            results.append(
                "✗ Unable to determine theory and open-ended module hours."
            )

    # ---------------------------------------------------------
    # MARK DISTRIBUTION
    # ---------------------------------------------------------
    if info["internal_marks"] == rule["internal_marks"]:
        results.append(
            f"✓ Internal marks correct ({info['internal_marks']})"
        )
    else:
        results.append(
            f"✗ Internal marks incorrect "
            f"(Expected: {rule['internal_marks']}, "
            f"Found: {info['internal_marks']})"
        )

    if info["external_marks"] == rule["external_marks"]:
        results.append(
            f"✓ External marks correct ({info['external_marks']})"
        )
    else:
        results.append(
            f"✗ External marks incorrect "
            f"(Expected: {rule['external_marks']}, "
            f"Found: {info['external_marks']})"
        )

        # ---------------------------------------------------------
    # INTERNAL MARK SPLIT VALIDATION
    # ---------------------------------------------------------
    split = info.get("internal_split", {})

    if split.get("theory_component_marks") is not None:
        checks = [
            (
                "Theory Component Marks",
                split["theory_component_marks"],
                rule["theory_component_marks"]
            ),
            (
                "Open-Ended Component Marks",
                split["open_ended_marks"],
                rule["open_ended_marks"]
            ),
            (
                "Test Marks (Theory)",
                split["test_theory"],
                rule["test_marks"]["theory"]
            ),
            (
                "Test Marks (Open-Ended)",
                split["test_open_ended"],
                rule["test_marks"]["open_ended"]
            ),
            (
                "Seminar Marks (Theory)",
                split["seminar_theory"],
                rule["seminar_marks"]["theory"]
            ),
            (
                "Seminar Marks (Open-Ended)",
                split["seminar_open_ended"],
                rule["seminar_marks"]["open_ended"]
            ),
            (
                "Assignment Marks (Theory)",
                split["assignment_theory"],
                rule["assignment_marks"]["theory"]
            ),
                (
                "Assignment Marks (Open-Ended)",
                split["assignment_open_ended"],
                rule["assignment_marks"]["open_ended"]
            ),
        ]

        all_correct = True

        for label, found, expected in checks:
            if found != expected:
                all_correct = False
                results.append(
                    f"✗ {label} incorrect (Expected: {expected}, Found: {found})"
                )

        if all_correct:
            results.append("✓ Internal mark split-up structure is correct")
    else:
        results.append("✗ Internal mark split-up could not be detected")

    return results
