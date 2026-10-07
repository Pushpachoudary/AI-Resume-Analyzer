import re

from skills import skills, skill_aliases


# -------------------------
# Find Skills
# -------------------------

def find_skills(text):

    text = text.lower()

    found_skills = []

    # -------------------------
    # Check Main Skills
    # -------------------------

    for skill in skills:

        skill_lower = skill.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(skill_lower)
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            if skill_lower not in found_skills:

                found_skills.append(
                    skill_lower
                )


    # -------------------------
    # Check Skill Aliases
    # -------------------------

    for alias, standard_skill in skill_aliases.items():

        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            if standard_skill not in found_skills:

                found_skills.append(
                    standard_skill
                )


    # -------------------------
    # Special Handling for R
    # -------------------------
    #
    # R is a single-character
    # programming language.
    #
    # It needs separate detection
    # to avoid false matches.
    #
    # Examples:
    #
    # "R programming"      -> match
    # "programming in R"   -> match
    # "R language"         -> match
    #
    # But:
    #
    # "resume"             -> no match
    # "react"              -> no match
    # "experience"         -> no match
    # -------------------------

    r_patterns = [

        r"\br programming\b",

        r"\bprogramming in r\b",

        r"\br language\b",

        r"\blanguage r\b",

        r"\br developer\b",

        r"\br development\b",

        r"\busing r\b",

        r"\bwith r\b"

    ]

    for pattern in r_patterns:

        if re.search(
            pattern,
            text
        ):

            if "r" not in found_skills:

                found_skills.append(
                    "r"
                )

            break


    return found_skills


# -------------------------
# Compare Skills
# -------------------------

def compare_skills(
    resume_skills,
    job_skills
):

    matched_skills = []

    missing_skills = []


    for skill in job_skills:

        if skill in resume_skills:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    if len(job_skills) > 0:

        match_percentage = (
            len(matched_skills)
            / len(job_skills)
        ) * 100

    else:

        match_percentage = 0


    return (
        matched_skills,
        missing_skills,
        match_percentage
    )


# -------------------------
# Generate Recommendations
# -------------------------

def generate_recommendations(
    missing_skills
):

    recommendations = []


    for skill in missing_skills:

        if skill.lower() == "python":

            recommendations.append(
                "Improve your Python programming skills."
            )


        elif skill.lower() == "sql":

            recommendations.append(
                "Practice SQL queries and database concepts."
            )


        elif skill.lower() == "fastapi":

            recommendations.append(
                "Learn FastAPI for building Python backend APIs."
            )


        elif skill.lower() == "git":

            recommendations.append(
                "Learn Git and GitHub for version control."
            )


        elif skill.lower() == "docker":

            recommendations.append(
                "Learn Docker basics and containerization."
            )


        elif skill.lower() == "mysql":

            recommendations.append(
                "Practice MySQL and relational database concepts."
            )


        elif skill.lower() == "postgresql":

            recommendations.append(
                "Learn PostgreSQL and relational database concepts."
            )


        elif skill.lower() == "tensorflow":

            recommendations.append(
                "Learn TensorFlow fundamentals for machine learning."
            )


        elif skill.lower() == "pytorch":

            recommendations.append(
                "Learn PyTorch fundamentals for deep learning."
            )


        elif skill.lower() == "aws":

            recommendations.append(
                "Learn AWS fundamentals and basic cloud services."
            )


        elif skill.lower() == "kubernetes":

            recommendations.append(
                "Learn Kubernetes fundamentals and container orchestration."
            )


        elif skill.lower() == "apache spark":

            recommendations.append(
                "Learn Apache Spark for large-scale data processing."
            )


        elif skill.lower() == "spark":

            recommendations.append(
                "Learn Apache Spark for large-scale data processing."
            )


        elif skill.lower() == "r":

            recommendations.append(
                "Learn R programming for statistical and data analysis."
            )


        else:

            recommendations.append(
                f"Consider learning {skill}."
            )


    return recommendations
