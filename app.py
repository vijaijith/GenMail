import streamlit as st
from mail import extract_text_from_pdf, generate_email
import urllib.parse

st.title("AI Email Drafter for Recruiters")

# --- Inputs ---
resume_file = st.file_uploader("Upload Resume (PDF)")
job_desc = st.text_area("Paste Job Description")
recruiter_email = st.text_input("Enter Recruiter's Email")

# --- Generate Email Button ---
if st.button("Generate Email"):
    if resume_file and job_desc:
        # Extract text from resume
        resume_text = extract_text_from_pdf(resume_file)

        # Generate subject and body from Gemini model
        sub_body_mail,subject, body = generate_email(resume_text, job_desc)

        st.subheader("Generated Email:")
        st.write(f"{sub_body_mail}")

        # --- Create Gmail draft link ---
        if recruiter_email and body:
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(body)
            gmail_url = (
                f"https://mail.google.com/mail/?view=cm&fs=1"
                f"&to={recruiter_email}&su={subject_encoded}&body={body_encoded}"
            )

            # Show a direct Gmail button
            st.link_button("📧 Draft this Email in Gmail", gmail_url)
        else:
            st.warning("Please enter the recruiter's email to draft the mail.")
    else:
        st.warning("Please upload resume and enter job description.")
