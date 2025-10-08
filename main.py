from src.logging import logger
from src.llm.LLM_Initalize import InitializeLLM
from src.Prompt.Templating import PromptTemplating
from src.Prompt.cleaning_to_csv import Cleaning_to_Csv
from src.utils.common import read_yaml_file


# Load text content
with open("data/content_text.txt", "r") as f:
    Text = f.read()

p = PromptTemplating()
raw_output= p.mcq_maker_prompt_Invoke(Text)
c = Cleaning_to_Csv()
c.cleaning(raw_output)