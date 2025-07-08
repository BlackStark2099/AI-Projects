from dotenv import load_dotenv
load_dotenv() ## this is basically meant for loading all the env variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input,image,prompt):
    response = gemini_model.generate_content([input,image[0],prompt])
    return response.text

# def input_image_setup(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.read()

#         image_parts =[
#            ContentPart(
#     inline_data=bytes_data,
#     mime_type=uploaded_file.type
# )

#         ]

#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        return [genai.upload_file(
            uploaded_file,
            mime_type=uploaded_file.type  # ✅ Required for file-like objects
        )]
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Gemini Demo")
st.header("Gemini LLM Application")

# User input
input = st.text_input("Enter your question:", key="input")
uploaded_file = st.file_uploader("Upload an image of the invoice (optional)", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image : ",use_container_width=True)

submit = st.button("Telle me about the invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is :")
    st.write(response)
