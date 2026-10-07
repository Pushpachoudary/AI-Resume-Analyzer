def read_job_description(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    return text


job_text = read_job_description("../data/job_description.txt")

print("JOB DESCRIPTION:")
print(job_text)