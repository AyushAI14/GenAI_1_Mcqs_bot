from src.logging import logger
from src.Prompt.Templating import PromptTemplating
import json, re
import pandas as pd


class Cleaning_to_Csv:
    def __init__(self):
        self.invoker = PromptTemplating()
        logger.info("PromptTemplating initialized.")

    def cleaning(self):
        logger.info("Cleaning process started.")
        try:
            text = self.invoker.mcq_maker_prompt_Invoke().strip()
            text = re.sub(r"^```(?:json)?", "", text)
            text = re.sub(r"```$", "", text)
            text = text.strip()
            logger.info("Response cleaned successfully.")

            df = pd.DataFrame(json.loads(text)).T
            df.to_csv('data/mcq.csv', index=False)
            logger.info("MCQs saved to data/mcq.csv.")

        except Exception as e:
            logger.error(f"Error during cleaning: {e}")


if __name__ == "__main__":
    c = Cleaning_to_Csv()
    c.cleaning()
