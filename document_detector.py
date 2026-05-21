import re


def detect_document_type(text):

    matches = re.findall(
        r'BCA\d[A-Z]{2,6}\d{2,3}',
        text
    )

    unique_codes = set(matches)

    if len(unique_codes) > 2:
        return "full_syllabus"

    return "single_course"
