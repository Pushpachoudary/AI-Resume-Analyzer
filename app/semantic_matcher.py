from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

from matcher import find_skills


# -------------------------
# Load AI Model
# -------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -------------------------
# Clean Text
# -------------------------

def clean_text(text):

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")

    text = re.sub(
        r" +",
        " ",
        text
    )

    return text.strip()


# -------------------------
# Overall Semantic Similarity
# -------------------------

def calculate_similarity(
    resume_text,
    job_text
):

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embedding = model.encode(
        [job_text]
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )

    return float(
        similarity[0][0]
    )


# -------------------------
# Create Resume Evidence Units
# -------------------------

def create_resume_chunks(text):

    text = clean_text(text)

    lines = text.split("\n")

    chunks = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove bullet points
        line = re.sub(
            r"^[•●▪◦\-\*]+\s*",
            "",
            line
        )

        # Split lines containing multiple sentences
        sentences = re.split(
            r"(?<=[.!?])\s+",
            line
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # Ignore resume section headings
            if sentence.lower().rstrip(":") in [

                "education",
                "experience",
                "work experience",
                "projects",
                "skills",
                "core skills",
                "technical skills",
                "certifications",
                "achievements",
                "summary",
                "profile",
                "objective"

            ]:

                continue

            if len(sentence) >= 10:

                chunks.append(
                    sentence
                )

    return chunks


# -------------------------
# Check Likely Job Title
# -------------------------

def is_likely_job_title(line):

    line = line.strip()

    if not line:
        return False

    line_lower = line.lower()

    line_lower = re.sub(
        r"^[#\-\*\d\.\)]+\s*",
        "",
        line_lower
    ).strip()

    job_title_keywords = [

        "developer",
        "engineer",
        "software engineer",
        "software developer",
        "data scientist",
        "data analyst",
        "machine learning engineer",
        "ml engineer",
        "ai engineer",
        "backend developer",
        "backend engineer",
        "frontend developer",
        "frontend engineer",
        "full stack developer",
        "full stack engineer",
        "qa engineer",
        "test engineer",
        "software tester",
        "intern",
        "analyst",
        "associate",
        "consultant",
        "administrator",
        "architect",
        "designer",
        "devops engineer",
        "cloud engineer"

    ]

    for keyword in job_title_keywords:

        if keyword in line_lower:

            return True

    # Short heading-like lines
    if (
        len(line) <= 50
        and not re.search(
            r"[.!?,;:]",
            line
        )
        and len(line.split()) <= 6
    ):

        return True

    return False


# -------------------------
# Extract Job Requirements
# -------------------------

def extract_requirements(job_text):

    job_text = clean_text(
        job_text
    )

    lines = job_text.split("\n")

    requirements = []

    first_content_line = True

    for line in lines:

        line = line.strip()

        if not line:
            continue

        cleaned_line = re.sub(
            r"^#+\s*",
            "",
            line
        ).strip()

        # Skip the job title
        if first_content_line:

            first_content_line = False

            if is_likely_job_title(
                cleaned_line
            ):

                continue

        # Skip section headings
        if cleaned_line.lower() in [

            "requirements",
            "requirements:",
            "qualifications",
            "qualifications:",
            "responsibilities",
            "responsibilities:",
            "job requirements",
            "job requirements:",
            "required skills",
            "required skills:",
            "preferred qualifications",
            "preferred qualifications:",
            "skills",
            "skills:"

        ]:

            continue

        # Skip generic introduction
        if cleaned_line.lower().startswith(
            "we are looking for"
        ):

            continue

        # Remove bullets / numbering
        cleaned_line = re.sub(
            r"^[•●▪◦\-\*\d\.\)]+\s*",
            "",
            cleaned_line
        )

        cleaned_line = cleaned_line.strip()

        if cleaned_line:

            requirements.append(
                cleaned_line
            )

    return requirements


# -------------------------
# Detect Requirement Weight
# -------------------------

def get_requirement_weight(requirement):

    requirement_lower = (
        requirement.lower()
    )

    optional_phrases = [

        "is a plus",
        "are a plus",
        "preferred",
        "preferable",
        "nice to have",
        "nice-to-have",
        "good to have",
        "bonus",
        "optional",
        "would be a plus",
        "would be advantageous",
        "an advantage",
        "advantageous"

    ]

    for phrase in optional_phrases:

        if phrase in requirement_lower:

            return 0.3

    return 1.0


# -------------------------
# AI Requirement Similarity
# -------------------------

def calculate_requirement_similarity(
    resume_text,
    job_text
):

    resume_chunks = create_resume_chunks(
        resume_text
    )

    resume_skills = find_skills(
        resume_text
    )

    job_requirements = extract_requirements(
        job_text
    )

    if not resume_chunks:
        return []

    if not job_requirements:
        return []

    resume_embeddings = model.encode(
        resume_chunks
    )

    results = []

    for requirement in job_requirements:

        requirement_skills = find_skills(
            requirement
        )

        missing_requirement_skills = []

        for skill in requirement_skills:

            if skill not in resume_skills:

                missing_requirement_skills.append(
                    skill
                )

        requirement_embedding = model.encode(
            [requirement]
        )

        similarities = cosine_similarity(
            requirement_embedding,
            resume_embeddings
        )[0]

        best_index = similarities.argmax()

        best_similarity = similarities[
            best_index
        ]

        # Do not show unrelated resume evidence
        # when an explicitly required skill is missing.
        if missing_requirement_skills:

            best_sentence = (
                "Required skill not found in resume."
            )

        elif best_similarity < 0.40:

            best_sentence = (
                "No strong semantic match found."
            )

        else:

            best_sentence = (
                resume_chunks[
                    best_index
                ]
            )

        weight = get_requirement_weight(
            requirement
        )

        results.append({

            "requirement": requirement,

            "similarity": float(
                best_similarity
            ),

            "best_sentence": best_sentence,

            "weight": weight

        })

    return results


# -------------------------
# Calculate Weighted
# Requirement Coverage
# -------------------------

def calculate_requirement_coverage(
    requirement_results
):

    if not requirement_results:

        return 0.0

    weighted_score = 0.0
    total_weight = 0.0

    for result in requirement_results:

        similarity = result[
            "similarity"
        ]

        weight = result[
            "weight"
        ]

        weighted_score += (
            similarity * weight
        )

        total_weight += weight

    if total_weight == 0:

        return 0.0

    coverage = (
        weighted_score
        / total_weight
    )

    return float(
        coverage
    )
