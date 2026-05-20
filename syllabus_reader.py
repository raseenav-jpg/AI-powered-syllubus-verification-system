import re
from docx import Document


# ---------------------------------------------------------
# TEXT EXTRACTION
# ---------------------------------------------------------
def extract_text_from_docx(file_path):
    """
    Extract all text from paragraphs and tables.
    Returns a single combined text string.
    """
    doc = Document(file_path)
    parts = []

    # Paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            parts.append(para.text.strip())

    # Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if para.text.strip():
                        parts.append(para.text.strip())

    return "\n".join(parts)


# ---------------------------------------------------------
# NORMALIZATION
# ---------------------------------------------------------
def normalize_text(text):
    """
    Convert text to lowercase and normalize whitespace.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def has_any_section(text, possible_names):
    """
    Check whether any section title exists in the document.
    """
    normalized_text = normalize_text(text)

    for name in possible_names:
        if normalize_text(name) in normalized_text:
            return True

    return False


# ---------------------------------------------------------
# COURSE OUTCOMES
# ---------------------------------------------------------
def count_course_outcomes(text):
    """
    Count unique CO labels such as CO1, CO2, ..., CO8.
    """
    matches = re.findall(r'\bCO\s*[1-8]\b', text, re.IGNORECASE)
    unique_cos = set(m.upper().replace(" ", "") for m in matches)
    return len(unique_cos)


# ---------------------------------------------------------
# HOURS EXTRACTION FROM DETAILED SYLLABUS TABLE
# ---------------------------------------------------------
def extract_hours_from_detailed_syllabus(file_path):
    """
    Extract fixed/theory and open-ended hours from the Detailed Syllabus table.

    Rules:
    1. If the Hrs header contains an explicit pattern '(A+B)',
       use the values exactly as written.
       Examples:
           (48+12) -> fixed_hours = 48, open_ended_hours = 12
           (45+30) -> fixed_hours = 45, open_ended_hours = 30
           (36+9)  -> fixed_hours = 36, open_ended_hours = 9
           (50+10) -> fixed_hours = 50, open_ended_hours = 10

    2. If only a single total value is present:
           60 -> fixed_hours = 48, open_ended_hours = 12
           75 -> fixed_hours = 45, open_ended_hours = 30
           45 -> fixed_hours = 36, open_ended_hours = 9

    3. If any other single total value is found,
       the system cannot determine the split automatically.
       In that case, it returns:
           fixed_hours = None
           open_ended_hours = None
           total_hours = total value
           hours_error_message =
               "Please mention your theory and open-ended module hours "
               "separately in your Detailed Syllabus."
    """

    import re
    from docx import Document

    doc = Document(file_path)

    for table in doc.tables:
        if not table.rows:
            continue

        # Read text from the first two rows because many syllabus
        # documents split the header across two rows.
        header_parts = []

        rows_to_check = min(2, len(table.rows))

        for row_index in range(rows_to_check):
            for cell in table.rows[row_index].cells:
                cell_text = cell.text.strip()
                if cell_text:
                    header_parts.append(cell_text)

        header_text = " ".join(header_parts)
        header_text = " ".join(header_text.split())

        # Ensure this is the Detailed Syllabus table
        header_lower = header_text.lower()
        if "module" not in header_lower or "hrs" not in header_lower:
            continue

        # -----------------------------------------------------
        # Case 1: Explicit pattern such as (50+10), (48+12),
        #         (45+30), (36+9)
        # -----------------------------------------------------
        match = re.search(r'\((\d+)\s*\+\s*(\d+)\)', header_text)
        if match:
            fixed_hours = int(match.group(1))
            open_ended_hours = int(match.group(2))
            total_hours = fixed_hours + open_ended_hours
            return (
                fixed_hours,
                open_ended_hours,
                total_hours,
                None
            )

        # -----------------------------------------------------
        # Case 2: Single total value only
        # -----------------------------------------------------
        numbers = re.findall(r'\b\d+\b', header_text)

        for num in numbers:
            total_hours = int(num)

            # Standard institutional mappings
            if total_hours == 60:
                return 48, 12, 60, None

            if total_hours == 75:
                return 45, 30, 75, None

            if total_hours == 45:
                return 36, 9, 45, None

            # Unknown total value
            return (
                None,
                None,
                total_hours,
                "Please mention your theory and open-ended module "
                "hours separately in your Detailed Syllabus."
            )

    # Detailed Syllabus table not found
    return (
        None,
        None,
        None,
        "Detailed Syllabus table or Hrs column not found."
    )
# ---------------------------------------------------------
# MARKS
# ---------------------------------------------------------
def detect_marks(text):
    """
    Detect standard internal and external marks.
    """
    text_lower = text.lower()

    internal = 30 if "30" in text else None
    external = 70 if "70" in text else None

    return internal, external

def detect_internal_split(text):
    """
    Detect internal mark split values from syllabus text.
    Returns a dictionary with detected values.
    """

    import re

    # Normalize whitespace
    normalized = " ".join(text.split())

    # Extract all numbers from the text
    numbers = [int(n) for n in re.findall(r'\b\d+\b', normalized)]

    # Default return structure
    detected = {
        "theory_component_marks": None,
        "open_ended_marks": None,
        "test_theory": None,
        "test_open_ended": None,
        "seminar_theory": None,
        "seminar_open_ended": None,
        "assignment_theory": None,
        "assignment_open_ended": None,
    }

    # Known valid patterns
    patterns = [
    # Theory Only / Elective Theory
    [20, 10, 10, 4, 6, 4, 4, 2],

    # Theory + Practical
    [10, 20, 5, 10, 3, 6, 2, 4],
]

    # Check whether all values of a pattern are present
    for pattern in patterns:
        if all(value in numbers for value in pattern):
            detected["theory_component_marks"] = pattern[0]
            detected["open_ended_marks"] = pattern[1]
            detected["test_theory"] = pattern[2]
            detected["test_open_ended"] = pattern[3]
            detected["seminar_theory"] = pattern[4]
            detected["seminar_open_ended"] = pattern[5]
            detected["assignment_theory"] = pattern[6]
            detected["assignment_open_ended"] = pattern[7]
            break

    return detected

# ---------------------------------------------------------
# MAIN EXTRACTION FUNCTION
# ---------------------------------------------------------

def extract_syllabus_info(file_path):
    """
    Extract all relevant syllabus information.
    """
    text = extract_text_from_docx(file_path)

    # Extract hours directly from Detailed Syllabus table
    fixed_hours, open_ended_hours, total_hours, hours_error_message = \
        extract_hours_from_detailed_syllabus(file_path)

    internal_marks, external_marks = detect_marks(text)
    internal_split = detect_internal_split(text)

    info = {
        "text": text,

        # Sections
        "has_course_summary": has_any_section(
            text, ["Course Summary"]
        ),

        "has_course_outcomes": has_any_section(
            text, ["Course Outcomes", "Course Outcomes (CO)"]
        ),

        "has_detailed_syllabus": (
            has_any_section(text, ["Detailed Syllabus"])
            or (
                has_any_section(text, ["Module"])
                and has_any_section(text, ["Unit"])
                and has_any_section(text, ["Content"])
            )
        ),

        "has_mapped_co": has_any_section(
            text, ["Mapped CO"]
        ),

        "has_copo_pso_mapping": has_any_section(
            text,
            [
                "Mapping of COs with PSOs and POs",
                "Mapping of COs with POs and PSOs"
            ]
        ),

        "has_assessment_rubrics": has_any_section(
            text, ["Assessment Rubrics"]
        ),

        "has_references": has_any_section(
            text, ["Reference", "Reference:", "References"]
        ),

        # Course Outcomes
        "co_count": count_course_outcomes(text),

        # Hours from Detailed Syllabus table
        "fixed_hours": fixed_hours,
        "open_ended_hours": open_ended_hours,
        "total_hours": total_hours,
        "hours_error_message": hours_error_message,

        # Marks
       "internal_marks": internal_marks,
       "external_marks": external_marks,
       "internal_split": internal_split
    }

    return info
