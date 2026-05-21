import tempfile
import streamlit as st

from auto_validator import auto_validate
from similarity_engine import calculate_similarity

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI-Powered Syllabus Verification System",
    page_icon="📘",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("📘 AI-Powered Syllabus Verification System")

st.write(
    "Upload a syllabus document and validate it automatically."
)

# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------
col1, col2 = st.columns([4, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📂 Upload Syllabus File",
        type=["docx", "pdf"]
    )

with col2:
    st.write("")
    st.write("")

    validate_button = st.button(
        "✅ Validate",
        use_container_width=True
    )

# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------
if validate_button:

    if uploaded_file is None:
        st.error("Please upload a file.")

    else:

        # Save temporary file
        suffix = (
            ".pdf"
            if uploaded_file.name.lower().endswith(".pdf")
            else ".docx"
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        # Run AI validation
        auto_result = auto_validate(temp_path)

        results = auto_result["results"]

        # -------------------------------------------------
        # DOCUMENT TYPE
        # -------------------------------------------------
        if auto_result["document_type"] == "single_course":

            st.success(
                f"🤖 AI detected: "
                f"{auto_result['predicted_rule']}"
            )

        else:

            st.info(
                f"📚 Full Programme Syllabus Detected\n\n"
                f"Total Courses: "
                f"{auto_result['total_courses']}"
            )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------
        summary = calculate_similarity(results)

        st.subheader("📊 Validation Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Passed", summary["passed"])
        c2.metric("Failed", summary["failed"])
        c3.metric("Similarity", f"{summary['score']}%")
        c4.metric("Decision", summary["decision"])

        # -------------------------------------------------
        # FULL SYLLABUS
        # -------------------------------------------------
        if auto_result["document_type"] == "full_syllabus":

            st.subheader("📘 Programme Report")

            for i, course in enumerate(results):

                title = (
                    f"{course['course_code']} "
                    f"→ {course['predicted_rule']}"
                )

                with st.expander(title):

                    if course["status"] == "success":
                        st.success("Classification successful")
                    else:
                        st.error("Classification failed")

                    for line in course["validation_results"]:

                        if line.startswith("✓"):
                            st.success(line)
                        else:
                            st.error(line)

        # -------------------------------------------------
        # SINGLE COURSE
        # -------------------------------------------------
        else:

            st.subheader("📋 Detailed Report")

            for line in results:

                if line.startswith("✓"):
                    st.success(line)
                else:
                    st.error(line)

        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------
        st.subheader("💡 Recommendations")

        failures = [
            r for r in results
            if isinstance(r, str) and r.startswith("✗")
        ]

        if not failures:
            st.success(
                "Syllabus follows the required structure."
            )
        else:
            for f in failures:
                st.warning(f)
