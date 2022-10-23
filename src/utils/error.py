import logging

def catch(block, data, message):
    try:
        return block(data)
    except Exception as e:
        logging.warning(f'{message}. Detail: {e}')
