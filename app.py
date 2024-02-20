import streamlit as st
import io
import pdf2image
from PIL import Image
import google.generativeai as genai
import base64


genai.configure(api_key = st.secrets["GOOGLE_API_KEY"])
def get_gemini_response(input, pdf_content,prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise Exception("File type not supported")

# Streamlit APP
st.set_page_config(page_title="ATS Scanner", page_icon=":robot_face:")
st.title("ATS Scanner using Google's Gemini-Pro-Vision")
st.write("This app uses Google's Gemini-Pro-Vision to scan your resume and provide feedback on how to improve it for ATS systems.")
st.write("Please upload your resume in PDF format below.")
job_desc = st.text_area("Job Description", key = "Please enter the job description here.")
uploaded_file = st.file_uploader("Choose PDF version of your resume", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully")

abt = st.button("Tell Me about my Resume")
# skills = st.button("How to improve my Skills")
match = st.button("Percentage Match")

inp_1 = """You are an experienced HR with Tech experience in field of data science, full stack web development, 
data analytics. Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of applicant in relation to the specified job description."""

inp_2 = """You are a skilled ATS (Applicant Tracking System) scanner of data science, full stack web development,data analytics and deep ATS functionality.
Your task is to evaluate the provided resume against the job description for these profiles. Give me the percentage of match if the resume matches with job description.
First the output should come as percentage match, then the keywords missing and then the final thoughts."""

if abt:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(inp_1, pdf_content, job_desc)
        st.subheader("About my Resume")
        st.write(response)
    else:
        st.error("Please upload a PDF file")

# elif skills:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_setup(uploaded_file)
#         response = get_gemini_response(inp_1, pdf_content, job_desc)
#         st.subheader("Skills to improve")
#         st.write(response)
#     else:
#         st.error("Please upload a PDF file")

elif match:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(inp_2, pdf_content, job_desc)
        st.subheader("Match Percentage")
        st.write(response)
    else:
        st.error("Please upload a PDF file")