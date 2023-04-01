import os
import datetime

class BaseConfig:
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H-%M-%S")

    HOSTS_FILE = "domains.txt"
    THREADS_NUMBER = 5
    FIELDS = {
        "title": "",
        "url": "",
        "meta": ""
    }
    OUTPUT_FOLDER = "results"
    OUTPUT_FILE = f"{OUTPUT_FOLDER}\\Results_{date_string}_{time_string}.csv"
    LOG_FOLDER = "logs"
    LOG_FILE = f"{LOG_FOLDER}\\main.log"
    LOG_FILE_SIZE = 3


if not os.path.exists(BaseConfig.LOG_FOLDER):
    os.makedirs(BaseConfig.LOG_FOLDER)
if not os.path.exists(BaseConfig.OUTPUT_FOLDER):
    os.makedirs(BaseConfig.OUTPUT_FOLDER)    