import random
import logging
import time


def wait(delays = list(range(1, 5+1))):
    delay = random.choice(delays)
    logging.info(f'Wait {delay} seconds...')
    time.sleep(delay)
