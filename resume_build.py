from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Store your base resume in a separate file
BASE_RESUME_PATH = "base_resume.tex"

def optimize_resume(job_description: str) -> str:
    """Optimize resume based on job description"""
    
    # Read base resume
    with open(BASE_RESUME_PATH, 'r') as f:
        base_resume = f.read()
    
    # Initialize client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create prompt
    prompt = f"""Modify ONLY the Summary, Experience, and Skills sections to align with this job description.

Job Description:
{job_description}

Instructions:
1. Summary: Rewrite to emphasize relevant experiences (3-4 lines)
2. Experience: Keep titles/companies/dates. Rewrite bullets for relevance. 3-4 bullets per role.
3. Skills: Only relevant skills from job description. 4 categories, 4-6 items each. Categorize depending on the job description.
4. DO NOT MODIFY: Projects, Education, Publications sections
5. Return ONLY complete LaTeX code, no explanations or markdown formatting.

Base Resume:
{base_resume}"""
    
    # Call API
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4-turbo" or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an expert resume optimizer. You modify resumes to match job descriptions while maintaining professional quality. Always return only the LaTeX code without any markdown formatting or explanations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    # Extract and clean LaTeX code
    latex_code = response.choices[0].message.content
    latex_code = latex_code.replace("```latex", "").replace("```", "").strip()
    
    return latex_code

# Usage
if __name__ == "__main__":
    job_desc = """
    BlackStone eIT, a leading computer software company, is looking for a skilled and motivated AI & ML Engineer to join our innovative team. In this role, you will be at the forefront of developing and implementing state-of-the-art artificial intelligence (AI) and machine learning (ML) algorithms to enhance our product offerings and optimize business functions. You will work collaboratively with data scientists, software engineers, and product teams to translate complex data into actionable insights and effective machine learning models. Your expertise will play a pivotal role in driving data-driven decision-making within the organization. This is an exciting opportunity to work on high-impact projects that leverage the latest advancements in AI and ML technologies. Requirements Proven experience as an AI & ML Engineer or in a related field, with at least 3 years of experience. Strong understanding of machine learning algorithms, deep learning, natural language processing, and computer vision techniques. Proficiency in programming languages such as Python, Java, or R. Hands-on experience with ML frameworks and libraries (TensorFlow, Keras, PyTorch, etc.). Experience with data preprocessing, feature extraction, and model evaluation. Background in statistics and mathematics to enhance algorithm performance. Ability to work with large datasets and experience with big data technologies (Hadoop, Spark, etc.) is a plus. Excellent problem-solving skills, attention to detail, and a collaborative attitude. Strong verbal and written communication skills to convey technical concepts to non-technical stakeholders. A degree in Computer Science, Mathematics, Data Science, or a related field is preferred. Benefits Paid Time Off Performance Bonus Training & Development
    """
    
    optimized = optimize_resume(job_desc)
    
    # Save output
    with open("optimized_resume.tex", 'w') as f:
        f.write(optimized)
    
    print("✓ Resume optimized and saved to optimized_resume.tex")