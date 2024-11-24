import os
import json
import pandas as pd
import traceback
from uuid import UUID


from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback


#load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

#get the model of gemini-1.5-flash
llm = ChatGoogleGenerativeAI(api_key=API_KEY, model='gemini-1.5-flash', temperature=0.5)




#template str
TEMPLATE="""
    Text={text}
    You are an expert in MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.\
    Make sure the questions are not repeated and are relevant to the text.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide.\
    Ensure to make {number} MCQs and don't add extra json to the response.\
    ### RESPONSE_JSON:
    {response_json}
    """

#template for the input prompt
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)


#chain for the quiz generation
quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


#template for the evaluation prompt
TEMPLATE_EVALUATION="""
    You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
    You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity 
    if the quiz is not at per with the cognitive and analytical abilities of the students,\
    update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities Quiz_MCQs:
    {quiz}
    Check from an expert English Writer of the above quiz:
"""

#template for the evaluation prompt
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE_EVALUATION
)

#chain for the evaluation
evaluation_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

#sequential chain for the quiz generation and evaluation
generate_evaluate_chain = SequentialChain(chains=[quiz_chain, evaluation_chain], input_variables=["text", "number", "subject", "tone", "response_json"], output_variables=["quiz", "review"], verbose=True)