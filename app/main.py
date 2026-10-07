from resume_parser import extract_text_from_pdf
from job_parser import read_job_description
from matcher import (
    find_skills,
    compare_skills,
    generate_recommendations
)
from semantic_matcher import calculate_similarity
from database import save_match_result


# Get user input
resume_path = input("Enter resume PDF path: ")
job_path = input("Enter job description path: ")
job_title = input("Enter job title: ")


# Read resume
resume_text = extract_text_from_pdf(resume_path)

# Read job description
job_text = read_job_description(job_path)


# Find skills
resume_skills = find_skills(resume_text)
job_skills = find_skills(job_text)


# Compare skills
matched, missing, skill_percentage = compare_skills(
    resume_skills,
    job_skills
)


# Calculate semantic similarity
semantic_score = calculate_similarity(
    resume_text,
    job_text
)


# Calculate final score
final_score = (
    0.7 * (skill_percentage / 100)
    + 0.3 * semantic_score
) * 100


# Generate recommendations
recommendations = generate_recommendations(missing)


# Display results
print("\n========== RESUME ANALYSIS ==========")

print("\nResume Skills:")
print(resume_skills)

print("\nJob Skills:")
print(job_skills)

print("\nMatched Skills:")
print(matched)

print("\nMissing Skills:")
print(missing)

print("\nSkill Match:")
print(f"{skill_percentage:.2f}%")

print("\nSemantic Similarity:")
print(f"{semantic_score * 100:.2f}%")

print("\nFinal Match Score:")
print(f"{final_score:.2f}%")

print("\nRecommendations:")

for recommendation in recommendations:
    print("-", recommendation)


# Save result
resume_name = resume_path.split("\\")[-1]

save_match_result(
    resume_name,
    job_title,
    float(final_score)
)
