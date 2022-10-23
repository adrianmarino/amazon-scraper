import random
import logging


def wait(delays = list(range(1, 5))):
    delay = random.choice(delays)
    logging.info(f'Wait {delay} seconds...')