import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from PyPDF2 import PdfReader 
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from src.mcqgenerator.mcqgenerator import generate_evaluation
from src.mcqgenerator.logger import logging
from langchain_community.callbacks.manager import get_openai_callback


response_json = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

st.title("Your AI Assistant to Generate MCQ")

with st.form("User input"):
    uploaded_file=st.file_uploader("Upload pdf or txt file pls")

    mcq_count=st.number_input("Lemme know how many mcqs you want?",min_value=3,max_value=20)

    subject=st.text_input("Insert subject", max_chars=20)
    tone=st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    button=st.form_submit_button("Ready to create MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text = read_file(uploaded_file)
            with get_openai_callback() as cb:
                response = generate_evaluation(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(response_json),
                    }
                )

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error while generating MCQs.")
        
        else:
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}")    
            
            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                
                if quiz is not None:
                    # ✅ Convert `quiz` from JSON string to a proper list of dictionaries
                    #st.write(f"Quiz Raw Data (Before Processing): {quiz}")  # Debugging
                    table_data = get_table_data(quiz)
                    #st.write(f"Processed Table Data: {table_data}")     
                    
                    # ✅ Validate table_data before passing to DataFrame
                    if table_data and isinstance(table_data, list):
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)

                        st.text_area(label="Review", value=response.get("review", ""))
                    else:
                        st.error("Error: Table data is empty or incorrectly formatted.")
                        st.write(f"Debug Info: {table_data}")  # Debugging output
                else:
                    st.error("Error: 'quiz' key not found in response.")
            else:
                st.write(response)
