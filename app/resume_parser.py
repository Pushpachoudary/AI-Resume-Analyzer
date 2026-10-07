import fitz
from skills import skills


def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


resume_text = extract_text_from_pdf("../data/resume.pdf")

print("RESUME TEXT:")
print(resume_text)

print("\nSKILLS FOUND:")

for skill in skills:
    if skill.lower() in resume_text.lower():
        print(skill)
