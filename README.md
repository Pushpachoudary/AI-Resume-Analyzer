# AI Resume Analyzer & Job Matcher

An AI-assisted resume analysis tool that compares a resume with a job description and provides an explainable match analysis.

The application combines **rule-based skill matching** with **semantic similarity using Sentence Transformers** to identify explicit skill gaps and relevant resume evidence.

## Features

- Upload a resume in PDF format
- Upload a job description as a TXT file
- Detect technical skills from the resume and job description
- Calculate explicit skill match percentage
- Compare individual job requirements with resume evidence
- Use Sentence Transformers for semantic similarity
- Identify missing technical skills
- Generate learning recommendations for missing skills
- Store analysis results in MySQL
- View previous analyses through Analysis History
- Streamlit-based user interface

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
      Recommendations
              |
              v
          MySQL
