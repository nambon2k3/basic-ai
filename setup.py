from setuptools import find_packages, setup
setup(
    name='mcqgenerator',
    version='0.1',
    author='Nam',
    install_requires=['langchain', 'streamlit','python-dotenv', 'pypdf2', 'google-generativeai', 'langchain-google-genai', 'langchain-community'],
    packages=find_packages()
)