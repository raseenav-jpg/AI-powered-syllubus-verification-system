import re


def get_prefix(course_code):

    code = course_code.upper()

    keywords = [
        "DSC",
        "DSE",
        "CJ",
        "EJ",
        "MN",
        "FM",
        "FS",
        "FV",
        "OE",
        "ENG"
    ]

    for k in keywords:
        if k in code:
            return k

    match = re.search(
        r'\d([A-Z]{2,6})\d+$',
        code
    )

    if match:
        return match.group(1)

    return "UNKNOWN"


def classify_course(course_code, info):
    

    print("\n========== CLASSIFIER DEBUG ==========")

    print("COURSE CODE:", course_code)

    print("TYPE:", info.get("type_of_course"))

    

    print("======================================\n")

  

    prefix = get_prefix(course_code)

    credits = info.get("credits")
    hours = info.get("hours_per_week")

    course_type = info.get(
        "type_of_course"
    )

    if course_type:
        course_type = (
            course_type.upper().strip()
        )

         # -------------------------------------------------
    # MAJOR
    # -------------------------------------------------

    if (
        course_type in ["DSC", "MAJOR"]
        or prefix in ["CJ", "DSC"]
    ):

        course_title = (
            info.get("course_title")
            or ""
        )

        if "practical" in (
            course_title.lower()
        ):

            return "Major Theory+Practical"

        return "Major Theory"

    # -------------------------------------------------
    # MINOR
    # -------------------------------------------------

    elif (
        course_type == "MINOR"
        or prefix == "MN"
    ):

        return "Minor Theory"

    # -------------------------------------------------
    # ELECTIVE
    # -------------------------------------------------

    elif (
        course_type in ["DSE", "ELECTIVE"]
        or prefix in ["EJ", "DSE"]
    ):

        return "Elective Theory"

    # -------------------------------------------------
    # FOUNDATION
    # -------------------------------------------------

    elif (
        course_type in [
            "FOUNDATION",
            "GENERAL FOUNDATION"
        ]
        or prefix == "FM"
    ):

        return "General Foundation Theory"

    # -------------------------------------------------
    # INTERNSHIP / PROJECT
    # -------------------------------------------------

    elif (
        course_type in [
            "INTERNSHIP",
            "PROJECT"
        ]
        or prefix in ["FS", "FV"]
    ):

        return "Internship / Project"

    return None
