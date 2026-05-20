import tempfile
import pandas as pd
import streamlit as st
from course_predictor import predict_course_type
from syllabus_reader import extract_syllabus_info
from rules import ACADEMIC_RULES
from validator import validate_syllabus
from similarity_engine import calculate_similarity

# ---------------------------------------------------------
# PAGE CONFIGURATION
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
    "Upload a syllabus document and verify whether it follows "
    "the approved academic structure."
)

# ---------------------------------------------------------
# COURSE TYPE + FILE UPLOAD + VALIDATE BUTTON
# ---------------------------------------------------------
col1, col2, col3 = st.columns([2, 3, 1])

# ---------------------------------------------------------
# COURSE TYPE DROPDOWN
# ---------------------------------------------------------
with col1:
    rule_name = st.selectbox(
        "📘 Select Course Type",
        list(ACADEMIC_RULES.keys()),
        index=None,   # No default selection
        placeholder="Choose the appropriate course type",
        width=350
    )


# ---------------------------------------------------------
# FILE UPLOADER
# ---------------------------------------------------------
with col2:
    uploaded_file = st.file_uploader(
        "📂 Upload Syllabus File",
        type=["docx", "pdf"]
    )

# ---------------------------------------------------------
# AI COURSE TYPE SUGGESTION
# ---------------------------------------------------------
if uploaded_file is not None:

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".docx"
    ) as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    # Extract syllabus information
    info = extract_syllabus_info(temp_path)

    # Predict the most likely course type
    predicted_rule = predict_course_type(info)

    # Display suggestion
    if predicted_rule:
        st.info(
            f"🤖 AI Suggestion: This syllabus appears to be "
            f"**{predicted_rule}**.\n\n"
            f"Please select this course type from the dropdown."
        )

# ---------------------------------------------------------
# VALIDATE BUTTON
# ---------------------------------------------------------
with col3:
    st.write("")
    st.write("")
    validate_button = st.button(
        "✅ Validate",
        use_container_width=True
    )
# ---------------------------------------------------------
# OPTIONAL EXPECTED STRUCTURE DISPLAY
# ---------------------------------------------------------
show_structure = st.selectbox(
    "📘 Do you want to view the expected course structure?",
    ["No", "Yes"],
    index=0,
    width=250
)

if show_structure == "Yes":

    rule = ACADEMIC_RULES[rule_name]
    co_rules = rule["co_rules"]

    with st.expander(
        "📘 Expected Structure for Selected Course Type",
        expanded=True
    ):

        # Prepare table data
        table_data = {
            "Parameter": [
                "Category",
                "Type",
                "Credits",
                "Hours/Week",
                "Theory Hours",
                "Open-Ended/Practical Hours",
                "Total Hours",
                "Internal Marks",
                "External Marks",
                "Total Marks",
                "CO Range",
                "Recommended COs",
            ],

            "Expected Value": [
                rule.get("course_category", "Not Defined"),
                rule.get("course_type", "Not Defined"),
                rule.get("credits", "Not Defined"),
                rule.get("hours_per_week", "Not Defined"),
                rule.get("theory_hours", "Not Defined"),
                rule.get(
                    "practical_hours",
                    rule.get("open_ended_hours", "Not Defined")
                ),
                rule.get("total_hours", "Not Defined"),
                rule.get("internal_marks", "Not Defined"),
                rule.get("external_marks", "Not Defined"),
                rule.get("total_marks", "Not Defined"),
                f"{co_rules.get('min_allowed', '')}–"
                f"{co_rules.get('max_allowed', '')}",
                co_rules.get("default_expected", "Not Defined"),
            ]
        }

        # Create DataFrame
        df = pd.DataFrame(table_data)

        # Display structure table
        st.dataframe(
            df,
            width=500,
            height=420
        )

        # -------------------------------------------------
        # INTERNAL MARK SPLIT TABLE
        # -------------------------------------------------
        st.markdown("### 📝 Internal Mark Split-Up")

        split_df = pd.DataFrame({
            "Component": [
                "Theory Component",
                "Open-Ended Component",
                "Test (Theory)",
                "Test (Open-Ended)",
                "Seminar (Theory)",
                "Seminar (Open-Ended)",
                "Assignment (Theory)",
                "Assignment (Open-Ended)",
            ],
            "Marks": [
                rule.get("theory_component_marks", ""),
                rule.get("open_ended_marks", ""),
                rule["test_marks"]["theory"],
                rule["test_marks"]["open_ended"],
                rule["seminar_marks"]["theory"],
                rule["seminar_marks"]["open_ended"],
                rule["assignment_marks"]["theory"],
                rule["assignment_marks"]["open_ended"],
            ]
        })

        st.dataframe(
            split_df,
            width=500,
            height=320
        )
        
# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------
if validate_button:
    if uploaded_file is None:
        st.error("Please upload a syllabus file first.")
    else:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".docx"
        ) as tmp:
            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        # Run validation
        results = validate_syllabus(temp_path, rule_name)

        # Calculate summary
        summary = calculate_similarity(results)

        # -------------------------------------------------
        # DISPLAY RESULTS
        # -------------------------------------------------
        st.subheader("📊 Validation Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Passed", summary["passed"])
        c2.metric("Failed", summary["failed"])
        c3.metric("Similarity", f"{summary['score']}%")
        c4.metric("Decision", summary["decision"])

        # Detailed report
        st.subheader("📋 Detailed Report")

        for result in results:
            if result.startswith("✓"):
                st.success(result)
            else:
                st.error(result)

        # Recommendations
        st.subheader("💡 Recommendations")

        failures = [r for r in results if r.startswith("✗")]

        if not failures:
            st.success(
                "The syllabus is complete and follows the required format."
            )
        else:
            for failure in failures:
                st.warning(failure)
