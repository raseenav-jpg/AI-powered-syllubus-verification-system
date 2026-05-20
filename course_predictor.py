from rules import ACADEMIC_RULES


def predict_course_type(info):
    """
    Predict the most likely course type by comparing extracted
    syllabus information with rules.
    """

    for rule_name, rule in ACADEMIC_RULES.items():

        # Match total hours
        if info.get("total_hours") != rule.get("total_hours"):
            continue

        # Match internal marks
        if info.get("internal_marks") != rule.get("internal_marks"):
            continue

        # Match external marks
        if info.get("external_marks") != rule.get("external_marks"):
            continue

        # Match credits if available
        if (
            info.get("credits") is not None
            and rule.get("credits") is not None
            and info.get("credits") != rule.get("credits")
        ):
            continue

        # Match hours per week if available
        if (
            info.get("hours_per_week") is not None
            and rule.get("hours_per_week") is not None
            and info.get("hours_per_week") != rule.get("hours_per_week")
        ):
            continue

        return rule_name

    return None
