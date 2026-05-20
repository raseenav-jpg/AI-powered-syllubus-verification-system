# Academic Rules for AI Syllabus Verification System

# Common CO validation rule
CO_RULES = {
    "default_expected": 6,
    "min_allowed": 5,
    "max_allowed": 8,
    "strict_mode": False,
    "exact_required": 6
}

ACADEMIC_RULES = {

    # ==========================================================
    # 1. MAJOR THEORY + PRACTICAL
    # ==========================================================
    "Major Theory+Practical": {
        "course_category": "Major",
        "course_type": "Theory + Practical",
        "credits": 4,
        "hours_per_week": 5,
        "theory_hours": 45,
        "practical_hours": 30,
        "total_hours": 75,

        "internal_marks": 30,
        "external_marks": 70,
        "total_marks": 100,

        "co_rules": CO_RULES,

        # Internal split
        "theory_component_marks": 10,
        "open_ended_marks": 20,

        "test_marks": {
            "theory": 5,
            "open_ended": 10
        },
        "seminar_marks": {
            "theory": 3,
            "open_ended": 6
        },
        "assignment_marks": {
            "theory": 2,
            "open_ended": 4
        }
    },

    # ==========================================================
    # 2. MAJOR THEORY ONLY
    # ==========================================================
    "Major Theory": {
        "course_category": "Major",
        "course_type": "Theory Only",
        "credits": 4,
        "hours_per_week": 4,
        "theory_hours": 48,
        "practical_hours": 12,
        "total_hours": 60,

        "internal_marks": 30,
        "external_marks": 70,
        "total_marks": 100,

        "co_rules": CO_RULES,

        # Internal split
        "theory_component_marks": 20,
        "open_ended_marks": 10,

        "test_marks": {
            "theory": 10,
            "open_ended": 4
        },
        "seminar_marks": {
            "theory": 6,
            "open_ended": 4
        },
        "assignment_marks": {
            "theory": 4,
            "open_ended": 2
        }
    },

# ==========================================================
# 3. ELECTIVE THEORY ONLY
# ==========================================================
"Elective Theory": {
    # Academic structure
    "course_category": "Elective",
    "course_type": "Theory Only",
    "credits": 4,
    "hours_per_week": 4,

    # Hour distribution
    "theory_hours": 48,
    "practical_hours": 12,
    "total_hours": 60,

    # Marks
    "internal_marks": 30,
    "external_marks": 70,
    "total_marks": 100,

    # Course Outcome Rules
    "co_rules": CO_RULES,

    # Internal mark split
    "theory_component_marks": 20,
    "open_ended_marks": 10,

    # Detailed split
    "test_marks": {
        "theory": 10,
        "open_ended": 4
    },
    "seminar_marks": {
        "theory": 6,
        "open_ended": 4
    },
    "assignment_marks": {
        "theory": 4,
        "open_ended": 2
    }
},

    # ==========================================================
# 5. MINOR THEORY ONLY
# ==========================================================
"Minor Theory": {
    # Academic structure
    "course_category": "Minor",
    "course_type": "Theory Only",
    "credits": 4,
    "hours_per_week": 4,

    # Hour distribution
    "theory_hours": 48,          # Fixed theory hours
    "practical_hours": 12,       # Open-ended module hours
    "total_hours": 60,

    # Marks
    "internal_marks": 30,
    "external_marks": 70,
    "total_marks": 100,

    # Course Outcome Rules
    "co_rules": CO_RULES,

    # Internal mark split (same as theory-only courses)
    "theory_component_marks": 20,
    "open_ended_marks": 10,

    "test_marks": {
        "theory": 10,
        "open_ended": 4
    },
    "seminar_marks": {
        "theory": 6,
        "open_ended": 4
    },
    "assignment_marks": {
        "theory": 4,
        "open_ended": 2
    }
},



# ==========================================================
# 8. MINOR THEORY + PRACTICAL
# ==========================================================
"Minor Theory+Practical": {
    # Academic structure
    "course_category": "Minor",
    "course_type": "Theory + Practical",
    "credits": 4,
    "hours_per_week": 5,

    # Hour distribution
    "theory_hours": 45,          # Fixed theory hours
    "practical_hours": 30,       # Practical / Open-ended hours
    "open_ended_hours": 30,      # Same as practical hours
    "total_hours": 75,

    # Marks
    "internal_marks": 30,
    "external_marks": 70,
    "total_marks": 100,

    # Course Outcome Rules
    "co_rules": CO_RULES,

    # Internal mark split
    # Same as Major Theory + Practical
    "theory_component_marks": 10,
    "open_ended_marks": 20,

    "test_marks": {
        "theory": 5,
        "open_ended": 10
    },
    "seminar_marks": {
        "theory": 3,
        "open_ended": 6
    },
    "assignment_marks": {
        "theory": 2,
        "open_ended": 4
    }
},
    # ==========================================================
# 6. GENERAL FOUNDATION THEORY ONLY
# ==========================================================
"General Foundation Theory": {
    # Academic structure
    "course_category": "General Foundation",
    "course_type": "Theory Only",
    "credits": 3,
    "hours_per_week": 3,

    # Hour distribution
    "theory_hours": 36,          # Fixed theory hours
    "practical_hours": 9,        # Open-ended module hours
    "total_hours": 45,

    # Marks
    "internal_marks": 25,
    "external_marks": 50,
    "total_marks": 75,

    # Course Outcome Rules
    "co_rules": CO_RULES,

    # Internal mark split
    # (Update these values if your institution specifies a
    # different 25-mark internal split for General Foundation.)
    "theory_component_marks": 15,
    "open_ended_marks": 10,

    "test_marks": {
        "theory": 8,
        "open_ended": 4
    },
    "seminar_marks": {
        "theory": 4,
        "open_ended": 3
    },
    "assignment_marks": {
        "theory": 3,
        "open_ended": 3
    }
},



    # ==========================================================
# 7. GENERAL FOUNDATION THEORY + PRACTICAL
# ==========================================================
"General Foundation Theory+Practical": {
    # Academic structure
    "course_category": "General Foundation",
    "course_type": "Theory + Practical",
    "credits": 3,
    "hours_per_week": 4,

    # Hour distribution
    "theory_hours": 30,          # Fixed theory hours
    "practical_hours": 30,       # Practical / Lab hours
    "open_ended_hours": 0,       # No separate open-ended module
    "total_hours": 60,

    # Marks
    "internal_marks": 25,
    "external_marks": 50,
    "total_marks": 75,

    # Course Outcome Rules
    "co_rules": CO_RULES,

    # Internal mark split
    # Update these values if your institution specifies a
    # different 25-mark split for General Foundation practical courses.
    "theory_component_marks": 10,
    "open_ended_marks": 15,

    "test_marks": {
        "theory": 5,
        "open_ended": 8
    },
    "seminar_marks": {
        "theory": 3,
        "open_ended": 4
    },
    "assignment_marks": {
        "theory": 2,
        "open_ended": 3
    }
},

}
    
