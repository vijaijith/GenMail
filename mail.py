import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#------------extract text from pdf

import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    text = ""
    # Read file bytes instead of file path
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

#-----------------subject and body separation

def sub_body(email):
    lines = [line.strip() for line in email.splitlines() if line.strip()]  # remove empty lines

    # Try to find a subject line
    subject_line = next((line for line in lines if line.lower().startswith("subject:")), None)

    if subject_line:
        subject = subject_line.split(":", 1)[1].strip()  # get text after 'Subject:'
        # Body = everything after the subject line
        body_start = lines.index(subject_line) + 1
        body = "\n".join(lines[body_start:]).strip()
    else:
        # Fallback: no subject found, use default
        subject = "Job Application"
        body = "\n".join(lines).strip()

    return subject, body



#-----------generate Email

def generate_email(resume_text, job_desc):
    prompt = f"""
You are an expert AI Email Drafter specializing in creating **ATS-friendly, HR-optimized, and AI-detection-proof job application emails** for freshers. 
Your goal is to generate concise, professional, and highly personalized emails that are fully compliant with both AI-based filters and Applicant Tracking Systems (ATS).

Follow these rules strictly:

Tone & Style:
- Formal, confident, and polite.
- Human-like and natural; avoid robotic phrasing.
- Avoid generic filler phrases like “hardworking individual” or “team player”.
- No emojis, fancy symbols, or creative formatting.

Structure:
1. Start with a professional greeting.
2. Introduce the applicant briefly (name, applying role, intent).
3. Express genuine interest in the specific role and company.
4. Highlight 2–3 key relevant skills, achievements, or projects that match the job description.
5. Mention that the resume is attached for detailed review.
6. End with a polite closing and call to action (e.g., willingness to discuss further or attend an interview).

ATS & Keyword Optimization:
- Include relevant keywords from the job description naturally.
- Emphasize technical skills, tools, and processes relevant to the role.
- Highlight measurable achievements or results where possible.

Length:
- Maximum 120–150 words.
- Keep sentences concise, clear, and readable.

Output Requirements:
1. Professionally worded email subject line.
2. Email body text.

Inputs:
--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{job_desc}

Generate a polished, fresher-optimized email that satisfies all the above criteria.
"""


    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    #return response.text
    subject,body = sub_body(response.text)
    return response.text,subject,body