import os
import PyPDF2
import json
import traceback


def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text=""
            for page in range(pdf_reader.numPages):
                text+=pdf_reader.getPage(page).extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading pdf file: {e}")
    elif file.name.endswith('.txt'):
        try:
            text = file.read()
            return text
        except Exception as e:
            raise Exception(f"Error reading txt file: {e}")
    else:
        raise Exception(f"File format not supported: {file}")

def get_table_data(quiz_dict):
    try:
        #load the dictionary
        quiz_dict = json.loads(quiz_dict)

        quiz_table_data = []

        #iterate through the dictionary and append to the list
        for key, value in quiz_dict.items():
            mcq = value.get("mcq")
            options = "\n".join(
                [
                    f"{option}: {option_value}" 
                    for option, option_value in value.get("options").items()
                ]
            )
            correct = value.get("correct")
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
        return quiz_table_data

    except Exception as e:
        raise Exception(f"Error reading table data: {e}")
        return False