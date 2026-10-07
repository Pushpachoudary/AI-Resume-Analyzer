from semantic_matcher import (
    calculate_requirement_similarity
)


resume_text = """
I have experience with Python and SQL.
I worked with MySQL databases.
I developed REST APIs for backend applications.
I used Git and GitHub for version control.
I have experience building dashboards using Power BI.
"""


job_text = """
We are looking for a Junior Software Engineer.

Requirements:
Strong knowledge of Python and SQL.
Experience with FastAPI and REST APIs.
Knowledge of MySQL and Git.
Understanding of Docker is a plus.
"""


results = calculate_requirement_similarity(
    resume_text,
    job_text
)


for result in results:

    print(
        f"\nRequirement: "
        f"{result['requirement']}"
    )

    print(
        f"Similarity: "
        f"{result['similarity'] * 100:.2f}%"
    )

    print(
        "Best resume evidence:",
        result["best_sentence"]
    )