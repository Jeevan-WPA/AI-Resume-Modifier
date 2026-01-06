import shutil 
import os
import csv

# def copy_test_files():
#     """Copy test files to the output directory for testing purposes."""
#     src_dir = "./resume_template"
#     dest_dir = "./output_copy"
    
#     if not os.path.exists(dest_dir):
#         os.makedirs(dest_dir)
     
#     shutil.copytree(src_dir, dest_dir)
    
jobdetails = {
  "job_description": "BlackStone eIT, a leading computer software company, is looking for a skilled and motivated AI & ML Engineer to join our innovative team. In this role, you will be at the forefront of developing and implementing state-of-the-art artificial intelligence (AI) and machine learning (ML) algorithms to enhance our product offerings and optimize business functions. You will work collaboratively with data scientists, software engineers, and product teams to translate complex data into actionable insights and effective machine learning models. Your expertise will play a pivotal role in driving data-driven decision-making within the organization. This is an exciting opportunity to work on high-impact projects that leverage the latest advancements in AI and ML technologies. Requirements Proven experience as an AI & ML Engineer or in a related field, with at least 3 years of experience. Strong understanding of machine learning algorithms, deep learning, natural language processing, and computer vision techniques. Proficiency in programming languages such as Python, Java, or R. Hands-on experience with ML frameworks and libraries (TensorFlow, Keras, PyTorch, etc.). Experience with data preprocessing, feature extraction, and model evaluation. Background in statistics and mathematics to enhance algorithm performance. Ability to work with large datasets and experience with big data technologies (Hadoop, Spark, etc.) is a plus. Excellent problem-solving skills, attention to detail, and a collaborative attitude. Strong verbal and written communication skills to convey technical concepts to non-technical stakeholders. A degree in Computer Science, Mathematics, Data Science, or a related field is preferred. Benefits Paid Time Off Performance Bonus Training & Development",
  "job_title": "AI & ML Engineer",
  "company": "BlackStone eIT",
  "location": "Abu Dhabi",
  "url": "https://ae.indeed.com/q-ai-ml-engineer-jobs.html?vjk=7f29000f62f7f273",
  "status": "applied",
  "date_time": "2026-01-05 11:47:15"
}


def update_csv(csv_path,job):
    """Update CSV file with new job details if needed."""
    fieldnames = [
    "date_time",
    "company",
    "job_title",
    "location",
    "job_description",
    "url",
    "status"
]

    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(job)


update_csv("./jobs_applied.csv", jobdetails)