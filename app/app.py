import streamlit as st
import pymupdf

from matcher import (
    find_skills,
    compare_skills,
    generate_recommendations
)

from semantic_matcher import (
    calculate_requirement_similarity,
    calculate_requirement_coverage
)

from database import (
    save_match_result,
    get_match_history
)


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -------------------------
# Header
# -------------------------

st.title(
    "📄 AI Resume Analyzer"
)

st.write(
    "Analyze your resume against a job description "
    "using explicit skill matching and AI-based "
    "semantic requirement analysis."
)

st.divider()


# -------------------------
# Input Section
# -------------------------

st.header(
    "📥 Upload Documents"
)

col1, col2 = st.columns(2)


with col1:

    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )


with col2:

    job_file = st.file_uploader(
        "Upload Job Description",
        type=["txt"]
    )


job_title = st.text_input(
    "Job Title",
    placeholder="Example: Junior Software Engineer"
)


st.divider()


# -------------------------
# Analyze Button
# -------------------------

analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)


# -------------------------
# Analysis
# -------------------------

if analyze_button:

    # -------------------------
    # Validate Inputs
    # -------------------------

    if not resume_file:

        st.error(
            "Please upload your resume PDF."
        )

        st.stop()


    if not job_file:

        st.error(
            "Please upload a job description."
        )

        st.stop()


    if not job_title:

        st.error(
            "Please enter the job title."
        )

        st.stop()


    # -------------------------
    # Extract Resume Text
    # -------------------------

    try:

        document = pymupdf.open(
            stream=resume_file.read(),
            filetype="pdf"
        )

        resume_text = ""

        for page in document:

            resume_text += (
                page.get_text()
            )

        document.close()


    except Exception as error:

        st.error(
            "Unable to read the resume PDF."
        )

        st.caption(
            f"PDF error: {error}"
        )

        st.stop()


    # -------------------------
    # Extract Job Description
    # -------------------------

    try:

        job_text = (
            job_file
            .read()
            .decode("utf-8")
        )

    except Exception as error:

        st.error(
            "Unable to read the job description."
        )

        st.caption(
            f"File error: {error}"
        )

        st.stop()


    # -------------------------
    # Skill Extraction
    # -------------------------

    resume_skills = find_skills(
        resume_text
    )

    job_skills = find_skills(
        job_text
    )


    # -------------------------
    # Explicit Skill Comparison
    # -------------------------

    matched_skills, missing_skills, skill_percentage = (
        compare_skills(
            resume_skills,
            job_skills
        )
    )


    skill_percentage = float(
        skill_percentage
    )


    # -------------------------
    # AI Requirement Analysis
    # -------------------------

    with st.spinner(
        "Analyzing resume with AI..."
    ):

        requirement_results = (
            calculate_requirement_similarity(
                resume_text,
                job_text
            )
        )


    # -------------------------
    # AI Requirement Coverage
    # -------------------------

    requirement_coverage = (
        calculate_requirement_coverage(
            requirement_results
        )
    )


    requirement_coverage_percentage = (
        requirement_coverage * 100
    )


    # -------------------------
    # Final Match Score
    # -------------------------

    final_score = float(
        (
            0.6 * (skill_percentage / 100)
            + 0.4 * requirement_coverage
        ) * 100
    )


    # -------------------------
    # Recommendations
    # -------------------------

    recommendations = (
        generate_recommendations(
            missing_skills
        )
    )


    # -------------------------
    # Results
    # -------------------------

    st.header(
        "📊 Analysis Results"
    )


    st.write(
        f"**Job:** {job_title}"
    )


    # -------------------------
    # Score Cards
    # -------------------------

    col1, col2, col3 = st.columns(3)


    # -------------------------
    # Skill Match
    # -------------------------

    with col1:

        st.metric(
            "🎯 Skill Match",
            f"{skill_percentage:.2f}%"
        )

        progress_value = float(
            min(
                skill_percentage / 100,
                1.0
            )
        )

        st.progress(
            progress_value
        )


    # -------------------------
    # AI Requirement Coverage
    # -------------------------

    with col2:

        st.metric(
            "🤖 AI Requirement Coverage",
            f"{requirement_coverage_percentage:.2f}%"
        )

        progress_value = float(
            min(
                requirement_coverage,
                1.0
            )
        )

        st.progress(
            progress_value
        )


    # -------------------------
    # Overall Match
    # -------------------------

    with col3:

        st.metric(
            "🏆 Overall Match",
            f"{final_score:.2f}%"
        )

        progress_value = float(
            min(
                final_score / 100,
                1.0
            )
        )

        st.progress(
            progress_value
        )


    # -------------------------
    # Scoring Explanation
    # -------------------------

    st.caption(
        "Overall Match = 60% explicit skill match "
        "+ 40% AI requirement coverage."
    )


    st.divider()


    # -------------------------
    # Matched and Missing Skills
    # -------------------------

    col1, col2 = st.columns(2)


    # -------------------------
    # Matched Skills
    # -------------------------

    with col1:

        st.subheader(
            "✅ Matched Skills"
        )


        if matched_skills:

            for skill in matched_skills:

                st.write(
                    f"✓ {skill}"
                )

        else:

            st.write(
                "No matching skills found."
            )


    # -------------------------
    # Missing Skills
    # -------------------------

    with col2:

        st.subheader(
            "❌ Missing Skills"
        )


        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"• {skill}"
                )

        else:

            st.success(
                "No major skill gaps found!"
            )


    # -------------------------
    # AI Requirement Analysis
    # -------------------------

    st.divider()


    st.subheader(
        "🤖 AI Requirement Analysis"
    )


    st.write(
        "The AI model compares each job requirement "
        "with the most relevant evidence found in "
        "the resume."
    )


    # -------------------------
    # Analyze Each Requirement
    # -------------------------

    for result in requirement_results:

        requirement = result[
            "requirement"
        ]


        similarity = (
            result["similarity"] * 100
        )


        evidence = result[
            "best_sentence"
        ]


        # -------------------------
        # Find Skills in Requirement
        # -------------------------

        requirement_skills = find_skills(
            requirement
        )


        # -------------------------
        # Find Matched Skills
        # -------------------------

        matched_requirement_skills = []

        for skill in requirement_skills:

            if skill in resume_skills:

                matched_requirement_skills.append(
                    skill
                )


        # -------------------------
        # Find Missing Skills
        # -------------------------

        missing_requirement_skills = []

        for skill in requirement_skills:

            if skill not in resume_skills:

                missing_requirement_skills.append(
                    skill
                )


        # -------------------------
        # Requirement Heading
        # -------------------------

        st.markdown(
            f"### 📌 {requirement}"
        )


        # -------------------------
        # Skill-Level Analysis
        # -------------------------

        if requirement_skills:

            st.write(
                "**Skill-level analysis:**"
            )


            # -------------------------
            # Matched Skills
            # -------------------------

            if matched_requirement_skills:

                for skill in matched_requirement_skills:

                    st.write(
                        f"✅ **{skill}** — Matched"
                    )


            # -------------------------
            # Missing Skills
            # -------------------------

            if missing_requirement_skills:

                for skill in missing_requirement_skills:

                    st.write(
                        f"❌ **{skill}** — Missing"
                    )


        # -------------------------
        # AI Semantic Similarity
        # -------------------------

        st.write(
            f"**AI Evidence Similarity:** "
            f"{similarity:.2f}%"
        )

        st.caption(
            "This score measures how semantically similar "
            "the resume evidence is to the job requirement. "
            "It is not a percentage of skill proficiency."
        )


        # -------------------------
        # Evidence Level
        # -------------------------

        if similarity >= 60:

            level = (
                "🟢 Strong semantic evidence"
            )

        elif similarity >= 40:

            level = (
                "🟡 Moderate semantic evidence"
            )

        else:

            level = (
                "🔴 Weak semantic evidence"
            )


        st.write(
            level
        )


        # -------------------------
        # Resume Evidence
        # -------------------------

        if evidence == (
            "No strong semantic match found."
        ):

            st.caption(
                "No strong resume evidence found."
            )

        else:

            st.write(
                "**Resume Evidence:**"
            )

            st.info(
                evidence
            )


    # -------------------------
    # Skill Gap Summary
    # -------------------------

    st.divider()


    st.subheader(
        "🔎 Skill Gap Summary"
    )


    if missing_skills:

        st.write(
            "These skills were detected in the "
            "job description but were not explicitly "
            "detected in the resume:"
        )


        for skill in missing_skills:

            st.warning(
                f"Missing: {skill}"
            )

    else:

        st.success(
            "All explicitly detected job skills "
            "are present in the resume."
        )


    # -------------------------
    # Recommendations
    # -------------------------

    st.divider()


    st.subheader(
        "💡 Recommendations"
    )


    if recommendations:

        for recommendation in recommendations:

            st.info(
                recommendation
            )

    else:

        st.success(
            "No major skill improvements recommended."
        )


    # -------------------------
    # Save Result to MySQL
    # -------------------------

    resume_name = resume_file.name


    try:

        save_match_result(
            resume_name,
            job_title,
            float(final_score)
        )


        st.success(
            "✅ Analysis result saved to MySQL!"
        )


    except Exception as error:

        st.error(
            "Unable to save the result to MySQL."
        )

        st.caption(
            f"Database error: {error}"
        )
        
# -------------------------
# Analysis History
# -------------------------

st.divider()

st.header(
    "📚 Analysis History"
)

try:

    history = get_match_history()

    if history:

        history_data = []

        for record in history:

            history_data.append({

                "ID": record[0],

                "Resume": record[1],

                "Job Title": record[2],

                "Match Score": (
                    f"{float(record[3]):.2f}%"
                ),

                "Date": record[4]

            })


        st.dataframe(
            history_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No analysis history available yet."
        )


except Exception as error:

    st.error(
        "Unable to load analysis history."
    )

    st.caption(
        f"Database error: {error}"
    )
