import re


def extract_course_codes(text):
    """
    Extract all course codes from the syllabus.

    Examples:
    - BCA1CJ101
    - BCA5EJ301
    - BCA8MN304
    - BCA7FM201
    """

    pattern = r'\b[A-Z]{3,6}\d+[A-Z]{2,4}\d+\b'

    course_codes = re.findall(pattern, text)

    # Remove duplicates and sort
    return sorted(set(course_codes))


def extract_course_entries(text):
    """
    Returns a list of dictionaries with course code and category prefix.
    """

    course_codes = extract_course_codes(text)

    entries = []

    for code in course_codes:
        # Extract alphabetic category prefix between semester digit and last digits
        match = re.search(r'\d([A-Z]{2,4})\d+$', code)

        prefix = match.group(1) if match else "UNKNOWN"

        entries.append({
            "course_code": code,
            "prefix": prefix
        })

    return entries
