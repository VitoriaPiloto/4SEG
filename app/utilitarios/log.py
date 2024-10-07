import logging

logging.basicConfig(filename='log_acoes.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_action(action):
    logging.info(action)
