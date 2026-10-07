
````markdown
# AI Resume Analyzer & Job Matcher

An AI-assisted resume analysis tool that compares a resume with a job description and provides an explainable match analysis.

The application combines **rule-based skill matching** with **semantic similarity using Sentence Transformers** to identify explicit skill matches, missing skills, relevant resume evidence, and areas for improvement.

---

## Features

- Upload a resume in PDF format
- Upload a job description in TXT format
- Extract text from resumes using PyMuPDF
- Detect technical skills from resumes and job descriptions
- Calculate explicit skill match percentage
- Compare individual job requirements with resume evidence
- Use Sentence Transformers for semantic similarity
- Identify missing technical skills
- Generate learning recommendations for missing skills
- Store analysis results in MySQL
- View previous analyses through Analysis History
- Streamlit-based web interface
- Explainable AI evidence for individual job requirements

---

## How It Works

```text
Resume PDF + Job Description
              |
              v
        Text Extraction
              |
              v
       Skill Extraction
              |
              v
     Explicit Skill Matching
              |
              v
   Semantic Requirement Matching
              |
              v
       Explainable Results
              |
              v
      Skill Gap Analysis
              |
              v
       Recommendations
              |
              v
          MySQL
````

The application uses both traditional rule-based matching and AI-based semantic matching rather than relying on a single similarity score.

---

## Matching Approach

The application uses two complementary approaches to analyze the resume.

### 1. Explicit Skill Matching

Technical skills are detected from both the resume and job description using a predefined skill dictionary and skill aliases.

For example:

```text
Job Description:
Python, SQL, FastAPI, Docker

Resume:
Python, SQL, Git

Result:

Matched Skills:
Python
SQL

Missing Skills:
FastAPI
Docker
```

The explicit skill match percentage is calculated based on the number of recognized job-description skills that are also found in the resume.

### 2. Semantic Requirement Matching

The application uses the `all-MiniLM-L6-v2` Sentence Transformer model to compare individual job requirements with relevant resume text.

This helps identify resume evidence that is semantically related to a requirement even when the wording is not exactly the same.

For example:

```text
Job Requirement:
Experience developing Python backend applications.

Resume Evidence:
Developed backend services using Python for data processing.
```

Even though the wording differs, the semantic model can identify the relationship between the requirement and the resume evidence.

> **Note:** Semantic similarity measures textual/semantic similarity. It does not measure actual candidate proficiency or guarantee that a candidate satisfies a requirement.

---

## Overall Match Score

The application combines explicit skill matching and AI-based requirement coverage into an overall score.

The current weighting is:

```text
60% Explicit Skill Match
40% AI Requirement Coverage
```

The formula is:

```text
Overall Match =
    0.60 × Skill Match
    +
    0.40 × AI Requirement Coverage
```

The weighting is intentionally kept simple and transparent so that the score can be easily explained.

---

## AI Requirement Analysis

For each job requirement, the application provides:

* Job requirement
* Detected technical skills
* Missing skills, when applicable
* AI semantic similarity
* Relevant resume evidence
* Evidence level

Example:

```text
Requirement:
Experience with Python and REST APIs.

Detected Skills:
Python
REST API

Missing Skills:
None

AI Evidence Similarity:
72%

Resume Evidence:
Developed backend applications using Python and REST APIs.
```

The semantic similarity value should be interpreted as an **evidence similarity score**, not as a percentage of skill proficiency.

---

## Skill Gap Analysis

The application identifies technical skills that appear in the job description but are not detected in the resume.

Example:

```text
Matched:
Python
SQL
Git

Missing:
FastAPI
Docker
PostgreSQL
```

For missing skills, the application can also generate recommendations such as:

```text
Learn FastAPI for building Python backend APIs.

Learn Docker basics and containerization.

Practice PostgreSQL and relational database concepts.
```

---

## Analysis History

Completed analyses can be stored in MySQL.

The application records:

* Resume filename
* Job title
* Overall match score
* Analysis date and time

Previous analyses can then be viewed through the **Analysis History** section of the Streamlit application.

---

## Tech Stack

### Programming Language

* Python

### AI / NLP

* Sentence Transformers
* Scikit-learn
* `all-MiniLM-L6-v2`

### PDF Processing

* PyMuPDF

### Database

* MySQL
* MySQL Connector/Python

### Frontend

* Streamlit

### Configuration

* python-dotenv

### Version Control

* Git
* GitHub

---

## Project Structure

```text
AI-Resume-Analyzer/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── job_parser.py
│   ├── main.py
│   ├── matcher.py
│   ├── resume_parser.py
│   ├── semantic_matcher.py
│   ├── skills.py
│   └── test_semantic.py
│
├── data/
│   └── Local resume and job-description files
│
├── .gitignore
├── README.md
└── requirements.txt
```

> Personal resume files, job descriptions, virtual environments, and environment variables are excluded from the Git repository.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Pushpachoudary/AI-Resume-Analyzer.git
```

## 2. Navigate to the Project

```bash
cd AI-Resume-Analyzer
```

## 3. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Database Setup

The application uses MySQL to store analysis history.

## 1. Create the Database

Open MySQL and run:

```sql
CREATE DATABASE resume_analyzer;
```

## 2. Create the Results Table

```sql
CREATE TABLE match_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_name VARCHAR(255),
    job_title VARCHAR(255),
    match_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Environment Variables

Create a `.env` file in the project root directory:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=resume_analyzer
```

Replace:

```text
your_mysql_password
```

with your local MySQL password.

### Important

Do not commit the `.env` file to GitHub.

The `.env` file is excluded through `.gitignore`.

---

# Running the Application

From the project root directory, run:

```bash
streamlit run backend/app.py
```

Streamlit will start the application locally.

The interface allows you to provide:

* Resume PDF
* Job description TXT
* Job title

After uploading the files, the application performs the analysis and displays the results.

---

# Example Output

The application provides:

```text
Skill Match
AI Requirement Coverage
Overall Match

Matched Skills
Missing Skills

AI Requirement Analysis
    |
    ├── Requirement
    ├── Detected Skills
    ├── Missing Skills
    ├── AI Evidence Similarity
    └── Resume Evidence

Skill Gap Summary

Recommendations

Analysis History
```

---

# Example Analysis

Suppose the job description contains:

```text
Strong knowledge of Python and SQL.
Experience with REST APIs.
Knowledge of Docker and PostgreSQL.
```

And the resume contains:

```text
Python
SQL
REST APIs
Git
```

The application can identify:

```text
Matched Skills:
Python
SQL
REST API

Missing Skills:
Docker
PostgreSQL
```

It can then provide recommendations for the missing skills.

---

# Limitations

The application has several intentional limitations:

* Skill detection depends on the predefined skill dictionary.
* New or uncommon technologies may not be detected unless added to the skill dictionary.
* Semantic similarity does not measure actual skill proficiency.
* Resume formatting and unusual wording can affect text extraction.
* The current scoring formula is a weighted combination rather than a trained hiring prediction model.
* The system does not determine whether a candidate should be hired.
* The tool is intended to assist resume analysis and should not be treated as an automated hiring decision system.

---

# Future Improvements

Potential improvements include:

* Expand the skill and skill-alias dictionary
* Support DOCX resumes
* Improve job requirement extraction
* Add configurable scoring weights
* Improve semantic evidence ranking
* Add more detailed resume section analysis
* Add authentication and user accounts
* Add visual analytics for analysis history
* Add automated tests for matching edge cases
* Add support for more resume formats
* Deploy the application to a cloud platform
* Add an API layer for external integrations

---

# What I Learned

This project provided practical experience with:

* Python application development
* Text processing and information extraction
* Regular expressions
* Rule-based matching
* Natural Language Processing
* Sentence Transformers
* Semantic similarity
* Explainable AI concepts
* MySQL database integration
* Streamlit application development
* Environment variable management
* Git and GitHub
* Building an end-to-end AI-assisted application

---

# License

This project is intended for educational and portfolio purposes.

````

