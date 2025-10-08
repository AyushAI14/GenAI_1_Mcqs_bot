import os
import json
from src.logging import logger
from src.llm.LLM_Initalize import InitializeLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from src.utils.common import read_yaml_file

# Load response.json
with open("response.json", "r") as f:
    response_json = json.load(f)



mcq_maker_prompt = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming to the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs.
### RESPONSE_JSON
{response_json}
"""

class PromptTemplating:
    def __init__(self):
        self.param = read_yaml_file("param.yaml")
        self.llm_instance = InitializeLLM()

    def mcq_maker_prompt_Invoke(self, text):
        mcq_maker_prompt_template = PromptTemplate(
            input_variables=["text", "number", "subject", "tone", "response_json"],
            template=mcq_maker_prompt
        )

        mcq_chain = RunnableSequence(
            first=mcq_maker_prompt_template,
            last=RunnableLambda(self.llm_instance.InvokeLLM)
        )

        result = mcq_chain.invoke({
            "text": text,
            "number": self.param.run.number,
            "subject": self.param.run.subject,
            "tone": self.param.run.tone,
            "response_json": json.dumps(response_json, indent=2)
        })

        output = result.content if hasattr(result, "content") else result
        print(output)
        return output

p = PromptTemplating()
