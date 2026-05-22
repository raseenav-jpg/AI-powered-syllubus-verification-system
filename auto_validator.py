from syllabus_reader import (
    extract_syllabus_info,
    extract_syllabus_info_from_text,
    extract_text
)

from document_detector import (
    detect_document_type
)

from course_classifier import (
    classify_course
)

from validator import (
    validate_syllabus
)

from programme_splitter import (
    split_courses
)


def auto_validate(file_path):

    text = extract_text(file_path)

    document_type = detect_document_type(text)
    print("\n========== AUTO VALIDATOR ==========")

    print("DOCUMENT TYPE:", document_type)

    print("====================================\n")

    # =================================================
    # SINGLE COURSE
    # =================================================
    if document_type == "single_course":

        info = extract_syllabus_info(
            file_path
        )
        print("\n========== INFO ==========")
        print(info)
        print("================================\n")

        course_code = info.get(
            "course_code",
            ""
        )

        predicted_rule = classify_course(course_code,info)

        if predicted_rule is None:

            return {
                "document_type":
                "single_course",

                "predicted_rule": None,

                "results": [
                    "✗ Unable to determine course type."
                ]
            }

        results = validate_syllabus(
            text,
            predicted_rule,info
        )

        return {

            "document_type":
            "single_course",

            "predicted_rule":
            predicted_rule,

            "results":
            results
        }

        # =================================================
    # FULL SYLLABUS
    # =================================================

    else:

        courses = split_courses(text)

        all_results = []

        print(
            "\nTOTAL COURSES:",
            len(courses)
        )

        for course in courses:

            try:

                course_text = course["text"]

                # -----------------------------------------
                # Extract course info
                # -----------------------------------------

                info = (
                    extract_syllabus_info_from_text(
                        course_text
                    )
                )

                print(
                    "\nPROCESSING:",
                    info.get("course_code")
                )

                # -----------------------------------------
                # Classification
                # -----------------------------------------

                predicted_rule = classify_course(

                    course["course_code"],

                    info
                )

                # -----------------------------------------
                # Validation
                # -----------------------------------------

                if predicted_rule:

                    validation_results = (
                        validate_syllabus(

                            course_text,

                            predicted_rule,

                            info
                        )
                    )

                    all_results.append({

                        "course_code":
                        course["course_code"],

                        "course_text":
                        course_text,

                        "predicted_rule":
                        predicted_rule,

                        "validation_results":
                        validation_results,

                        "status":
                        "success"
                    })

                else:

                    all_results.append({

                        "course_code":
                        course["course_code"],

                        "course_text":
                        course_text,

                        "predicted_rule":
                        "Unable to classify",

                        "validation_results":
                        [
                            "✗ Classification failed"
                        ],

                        "status":
                        "error"
                    })

            except Exception as e:

                print(
                    "\nFULL SYLLABUS ERROR:",
                    str(e)
                )

                all_results.append({

                    "course_code":
                    course.get(
                        "course_code",
                        "UNKNOWN"
                    ),

                    "course_text":
                    course.get(
                        "text",
                        ""
                    ),

                    "predicted_rule":
                    "Processing Error",

                    "validation_results":
                    [
                        f"✗ {str(e)}"
                    ],

                    "status":
                    "error"
                })

        return {

            "document_type":
            "full_syllabus",

            "total_courses":
            len(courses),

            "results":
            all_results
        }
