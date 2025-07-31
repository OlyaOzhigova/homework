import functools
import logging


def simple_logger(func):
    logging.basicConfig(level=logging.INFO, filename='log.txt', filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(f"Function '{func.__name__}' called with args={args}, kwargs={kwargs}, returned {result}")
        return result

    return wrapper