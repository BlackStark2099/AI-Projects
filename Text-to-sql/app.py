from dotenv import load_dotenv 

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import sqlite3

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

gemini_model = genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(question,prompt):
    response = gemini_model.generate_content([prompt[0],question])
    return response.text

## function to retrive query from sql database

def read_sql_query(sql,db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
 

def read_sql_data(prompt,data):
    response = gemini_model.generate_content([prompt[1],data])
    return response.text

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, age,grade,attendance_percentage,pin, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """,
    """
    You are an intelligent data summarizer.

    I will provide you with SQL query results in table format. Your task is to:

    Understand the data in the table.

    Convert it into a clear, concise, and human-readable summary.

    Highlight key insights, counts, groupings, or trends if they are evident.

    Use simple language that any stakeholder can understand.

    and answer should be contextual to the question which the user has asked for

    """
]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    response=read_sql_query(response,"student.db")
    response = {
        'response' : response,
        'question' : question
    }
    response = read_sql_data(prompt,str(response))
    st.subheader("The REsponse is")
    st.write(response)