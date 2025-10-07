import logging
import os
import sys

formatting = "[%(asctime)s | %(levelname)s in %(module)s: %(message)s]"
filepath = os.path.join('log','looping.log')
os.makedirs('log',exist_ok=True)

logging.basicConfig(
    format=formatting,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(filepath)
    ]
)

logger = logging.getLogger('mcq_bot')