from langchain_openai import OpenAI 
from langchain_openai import OpenAI  
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_core.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback  
from langchain_openai import ChatOpenAI
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

key=os.getenv("openai_key")

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-4",temperature=0.8)

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

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_template=PromptTemplate(
    input=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)

quiz_chain=LLMChain(llm=llm, prompt=quiz_template, output_key="quiz")

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review")

generate_evaluation=SequentialChain(chains=[quiz_chain,review_chain],input_variables=['text','number','subject','tone','response_json'], output_variables=['quiz','review'])

