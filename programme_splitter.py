import re


def split_courses(text):

    courses = []

    # Split using Course Code pattern
    pattern = r'(Course\s*Code\s*[A-Z0-9]+)'

    parts = re.split(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    # Merge heading + content
    for i in range(1, len(parts), 2):

        heading = parts[i]

        content = ""

        if i + 1 < len(parts):

            content = parts[i + 1]

        full_text = (
            heading + "\n" + content
        )

        # Extract course code
        match = re.search(

            r'Course\s*Code\s*([A-Z0-9]+)',

            heading,

            re.IGNORECASE
        )

        if match:

            course_code = (
                match.group(1)
            )

        else:

            course_code = "UNKNOWN"

        courses.append({

            "course_code":
            course_code,

            "text":
            full_text
        })

    print(
        "\nTOTAL COURSES FOUND:",
        len(courses)
    )

    return courses
