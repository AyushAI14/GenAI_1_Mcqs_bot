from setuptools import setup, find_packages

setup(
    name="MCQs_Generator",
    version="0.1.0",
    packages= find_packages(),
    install_requires=[
        'langchain', 
        'langchain_google_genai', 
        'langchain_core', 
        'pandas', 
        'fastapi',
        'setuptools'
    ],
)
