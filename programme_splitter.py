import re


def split_courses(text):

    pattern = r'(BCA\d[A-Z]{2,6}\d{2,3})'

    matches = list(
        re.finditer(pattern, text)
    )

    courses = []

    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        course_text = text[start:end]

        courses.append({
            "course_code": match.group(1),
            "text": course_text
        })

    return courses
