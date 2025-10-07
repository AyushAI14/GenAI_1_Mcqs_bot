from pathlib import Path
import yaml
from src.logging import logger
from box import Box


def read_yaml_file(filepath : str):
    try:
        with open(filepath,'r') as f:
            content = yaml.safe_load(f)
            logger.debug('Yaml File has loaded Successfully')
            return Box(content)
    except Exception as e:
        logger.debug(f'Unable to load the yaml file from {filepath}')

