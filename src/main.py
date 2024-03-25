from datetime import datetime
import os
import shutil
import time
import utils


def get_files_from_directory(directory: str) -> dict[str, dict]:
    '''    
    Get a dict with the files in directory : {'name of file': {'size': int}}

            Parameters:
                    directory (str): A decimal integer
            Returns:
                    items_dict (dict): {'name of file': {'size': int}}
    '''
    if not isinstance(directory, str):
        raise TypeError

    contents: list = os.listdir(directory)
    items_dict: dict = {}

    for item in contents:
        path = os.path.join(directory, item)
        file_stats = os.stat(path)
        items_dict[item] = {'size': file_stats.st_size}

    return items_dict


def check_file_existance_and_modifications(
    source_files: dict, 
    replica_files: dict, 
    source: str, 
    replica: str
) -> None:
    '''    
    Check if the files exists in replica and if they were modified in source. 
    If so, copy file to replica again.

            Parameters:
                   source_files (dict):{'name of file': {'size': int}}
                   replica_files (dict):{'name of file': {'size': int}}
                   source (str): The path do source directory 
                   replica (str): The path do replica directory 
            Returns:
                    None
    '''
    for file in source_files:
        file_path: str = os.path.join(source, file)
        if file not in replica_files:
            shutil.copy(file_path, replica)
            logger.info(f' The file with the name {file} was copied')
        else:
            #changes in the file by size
            if replica_files[file]['size'] != source_files[file]['size']:
                os.remove(os.path.join(replica, file))
                shutil.copy(file_path, replica)
                logger.info(f' The file with the name {file} was modified')
            #changes in the file by MD5
            elif utils.compare_file_content_md5(source, file, replica):
                os.remove(os.path.join(replica, file))
                shutil.copy(file_path, replica)
                logger.info(f' The file with the name {file} was modified')


def delete_files_from_replica(source_files: dict, replica_files: dict, replica: str) -> None:
    '''    
    Delete Files from replica if file does not exist in source anymore.

            Parameters:
                   source_files (dict):{'name of file': {'size': int}}
                   replica_files (dict):{'name of file': {'size': int}}
                   replica (str): The path do replica directory 
            Returns:
                    None
    '''
    for file_name in replica_files:
        if file_name not in source_files:
            os.remove(os.path.join(replica, file_name))
            logger.info(f' The file with the name {file_name} was deleted')


def compare_files_in_source_and_replica(source: str, replica: str) -> None:
    '''    
    Comparing files in both source and replica.

            Parameters:
                source (str): The path do source directory 
                replica (str): The path do replica directory 
            Returns:
                None
    '''
    source_files: dict = get_files_from_directory(source)
    replica_files: dict = get_files_from_directory(replica)

    #to check for presence or modifications on files
    check_file_existance_and_modifications(source_files, replica_files, source, replica)

    #to delete files
    delete_files_from_replica(source_files, replica_files, replica) 



if __name__ == "__main__":
    args = utils.given_arguments_cmd_line()

    logger = utils.logger_config(
        logger_name='fileSync',
        logger_path=args.log,
        logger_file_name=datetime.now().strftime("%m_%d_%Y")
    )

    try:
        # Create the directory
        if not os.path.exists(args.dst):
            os.mkdir(args.dst)
            logger.info(f'The directory with the name {args.dst} was created')

        if args.interval < 0:
            compare_files_in_source_and_replica(args.src, args.dst)
                
        else:
            while True:
                compare_files_in_source_and_replica(args.src, args.dst)
                time.sleep(args.interval)
    except Exception as e:
        logger.debug('Unexpected Error', exc_info=True)
        logger.info('Unexpected Error.')