import os

import mysql.connector
from dotenv import load_dotenv


# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()


# -------------------------
# Database Connection
# -------------------------

def connect_to_database():

    connection = mysql.connector.connect(

        host=os.getenv("DB_HOST"),

        port=int(
            os.getenv(
                "DB_PORT",
                "3306"
            )
        ),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD"),

        database=os.getenv("DB_NAME")

    )

    return connection


# -------------------------
# Save Match Result
# -------------------------

def save_match_result(
    resume_name,
    job_title,
    match_score
):

    connection = connect_to_database()

    cursor = connection.cursor()

    query = """
    INSERT INTO match_results
    (
        resume_name,
        job_title,
        match_score
    )
    VALUES
    (
        %s,
        %s,
        %s
    )
    """

    values = (
        resume_name,
        job_title,
        match_score
    )

    cursor.execute(
        query,
        values
    )

    connection.commit()

    cursor.close()

    connection.close()

    print(
        "Match result saved successfully!"
    )


# -------------------------
# Get Match History
# -------------------------

def get_match_history():

    connection = connect_to_database()

    cursor = connection.cursor()

    query = """
    SELECT
        id,
        resume_name,
        job_title,
        match_score,
        created_at
    FROM match_results
    ORDER BY created_at DESC
    """

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()

    connection.close()

    return results