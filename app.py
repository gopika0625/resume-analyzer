import streamlit as st
from PyPDF2 import PdfReader
import datetime

# Page settings
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume based on job roles")

# Job roles and skills
roles = {
    "Data Scientist": ["python", "machine learning", "data science", "numpy", "pandas", "sql"],
    "Web Developer": ["html", "css", "javascript", "react", "node", "mongodb"],
    "Software Engineer": ["java", "c++", "data structures", "algorithms", "sql"]
}

# Select role
role = st.selectbox("Select Job Role", list(roles.keys()))

# Upload PDF
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    text = text.lower()

    skills = roles[role]

    found_skills = [skill for skill in skills if skill in text]
    missing_skills = [skill for skill in skills if skill not in text]

    score = int((len(found_skills) / len(skills)) * 100)

    st.subheader("📊 Resume Score")
    st.progress(score)
    st.write(f"Score: {score}%")

    st.subheader("✅ Skills Found")
    st.write(found_skills)

    st.subheader("❌ Missing Skills")
    st.write(missing_skills)

    st.subheader("💡 Suggestions")
    if score > 70:
        st.success("Great resume! You're on the right track.")
    else:
        st.warning("Improve your resume by adding missing skills.")

    # Save results
    with open("results.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | Role: {role} | Score: {score}%\n")

# Show previous results
if st.checkbox("Show Previous Results"):
    try:
        with open("results.txt", "r") as f:
            st.text(f.read())
    except:
        st.write("No history available yet.")