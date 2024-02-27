import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

__formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')

__console = logging.StreamHandler(stream=sys.stdout)
__console.setLevel(logging.INFO)
__console.setFormatter(__formatter)
logger.addHandler(__console)
