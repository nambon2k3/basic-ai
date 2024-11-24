import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging




#loading json file
with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

#creating a title
st.title("MCQ Generator")

#create a form using streamlit
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Choose a file (PDF or txt): ")

    #input fields
    mcq_count = st.number_input("Number of MCQs", min_value=1, max_value=10, value=5)
    #input subject
    subject = st.text_input("Subject", "English")

    #input tone 
    tone = st.selectbox("Tone", ["Simple", "Mediate", "Complex"])

    #submit button
    submitted = st.form_submit_button("Create MCQs")

    #if the form is submitted
    if submitted and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                #read the file
                text = read_file(uploaded_file)
                #generate and evaluate the MCQs
                with get_openai_callback() as callback:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                logging.error(f"Error generating MCQs: {e}")
                st.error(f"Error generating MCQs2: {e}")
            else:
                print (f"Total Tokens: {callback.total_tokens}") 
                print(f"Prompt Tokens:{callback.prompt_tokens}")
                print (f"Completion Tokens: {callback.completion_tokens}")
                print (f"Total Cost: {callback.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    if quiz is not None:
                        #clean quiz data to format to json
                        cleaned_quiz = quiz.replace("```json\n", "").strip()
                        cleaned_quiz = cleaned_quiz.replace("```", "").strip()

                        #display the table data     
                        table_data = get_table_data(cleaned_quiz)  
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index += 1
                            st.table(df)
                            #display review box
                            st.text_area(label="Review", value=response.get("review"))   
                        else:
                            st.error("Error displaying table data")
                else:
                    st.write(response)
                
                