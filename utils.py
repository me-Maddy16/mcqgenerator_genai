import os
import PyPDF2
import json
import traceback

from PyPDF2 import PdfReader

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:  # Prevent NoneType errors
                    text += extracted_text
            return text if text.strip() else "No readable text found in PDF."
        except Exception as e:
            raise Exception(f"Error reading the PDF file: {e}")
    
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")  # Decode only if necessary
        except AttributeError:
            return file.read()  # If already a string

    else:
        raise Exception("Unsupported file format. Only PDF and TXT files are supported.")

import json
import traceback

def get_table_data(quiz_input):
    try:
        # ✅ Handle both string and dictionary inputs
        if isinstance(quiz_input, str):
            quiz_dict = json.loads(quiz_input)  # Convert JSON string to dict
        elif isinstance(quiz_input, dict):
            quiz_dict = quiz_input  # Already a dictionary, no need to parse
        else:
            raise ValueError("Invalid data type for quiz input.")

        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "No question found")
            options_dict = value.get("options", {})
            correct = value.get("correct", "No correct answer provided")

            options = " || ".join(
                [f"{option}-> {option_value}" for option, option_value in options_dict.items()]
            )

            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data if quiz_table_data else False  # Ensure non-empty data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False