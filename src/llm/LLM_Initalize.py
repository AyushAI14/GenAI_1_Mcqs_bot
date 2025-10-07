import os
from src.utils.common import read_yaml_file
from src.logging import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


class InitializeLLM:
    def __init__(self):
        self.param = read_yaml_file('param.yaml')
        self.API_KEY = os.getenv('GEMINI_APIKEY')
        self.Model = self.param.model.name
        # self.load_llm()

    def load_llm(self):
        try:
            llm = ChatGoogleGenerativeAI(
            api_key=self.API_KEY,
            model=self.Model,
            max_output_tokens=self.param.model.max_output_tokens,
            temperature=self.param.model.temperature)
            logger.info(f"{self.param.model.name} has been Initialized")
        except Exception as e:
            logger.info('Unable to load the LLM Model',e)
    
    def InvokeLLM(self,prompt:str):
        try:
            llm = ChatGoogleGenerativeAI(
            api_key=self.API_KEY,
            model=self.Model,
            max_output_tokens=self.param.model.max_output_tokens,
            temperature=self.param.model.temperature)
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.info('LLM Model is unable to respond',e)

llm_1 = InitializeLLM()