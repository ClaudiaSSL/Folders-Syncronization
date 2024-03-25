import hashlib
import logging
import os
import argparse
from argparse import Namespace
from logging import Logger

def logger_config(logger_name: str, logger_path: str, logger_file_name: str) -> Logger:
    '''    
    Configuring logger

            Parameters:
                    logger_name (str):  Name of the logger
                    logger_path (str): Path to log file
                    logger_file_name (str): Name to log file
            Returns:
                    logger (variable)
    '''
    if not os.path.exists(logger_path):
        os.mkdir(logger_path)

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().handlers.clear()

    logger = logging.getLogger(logger_name)
    log_formatter = logging.Formatter('%(asctime)s %(message)s')

    file_handler = logging.FileHandler(f'{logger_path}/{logger_file_name}.verbose.log')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    return logger



def read_file(file_path: str) -> bytes:
    '''    
    Open and close file

            Parameters:
                    file_path (str): A path to file to be open
            Returns:
                    file (TextIOWrapper): TextIOWrapper
    '''

    with open(file_path, "rb") as file:
        temp = file.read()
    return temp

def compare_file_content_md5(source: str, file_name: str, replica: str) -> bool:
    '''    
    Check file modifications with MD5

            Parameters:
                source (str): The path do source directory 
                file_name (str): The name of the file
                replica (str): The path do replica directory 
            Returns:
                bool
    '''

    source_file_path: str= os.path.join(source, file_name)
    replica_file_path: str = os.path.join(replica, file_name)

    source_file: bytes = read_file(source_file_path)
    replica_file: bytes = read_file(replica_file_path)

    md5_source_file: str = hashlib.md5(source_file).hexdigest()  
    md5_replica_file: str = hashlib.md5(replica_file).hexdigest()
    
    return md5_source_file != md5_replica_file

def given_arguments_cmd_line() -> Namespace:
    '''    
    Get a dict with the files in directory : {'name of file': {'size': int}}

           Returns:
                    parametersList (list): list of parameters [folder paths, sync_period, log file path]
    '''
    #argument_list: list = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Folder Syncronizer')
    parser.add_argument('src', help='Source folder')
    parser.add_argument('dst', help='Destination folder')
    parser.add_argument('-l','--log', default='./logs')
    parser.add_argument(
        '-i',
        '--interval', 
        default=-1, 
        type=int,
        help=(
            'The interval (in seconds) in which the program will do the sync rotine.' 
            'If none is provided, an adhoc sync will be performed.'
        )
    )
    args = parser.parse_args()
    return args