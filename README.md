# Folders-Syncronization
Maintain a full, identical copy of source folder at replica folder

## Installation

No instalation required

## Usage

Folder Syncronizer

    positional arguments:
  src                   Source folder
  dst                   Destination folder

optional arguments:
  -h, --help            show this help message and exit
  -l LOG, --log LOG
  -i INTERVAL, --interval INTERVAL
                        The interval (in seconds) in which the program will do the sync routine.If none is provided, an adhoc sync will be performed.

### Test

adhoc sync: 
    ```bash
    python src/main.py tests_folder/source tests_folder/rep_dir 
    ```

if you want to run on the background every 60 seconds 
    ```bash
    python src/main.py tests_folder/source tests_folder/rep_dir -i 60 &
    ```


