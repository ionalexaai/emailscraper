import os

class BaseConfig:
    HOSTS_FILE = ""
    FIELDS = {
        "title": "",
        "url": "",
        "meta": ""
    }
    OUTPUT_FILE = ""
    LOG_FOLDER = "logs"
    LOG_FILE = f"{LOG_FOLDER}\\main.log"
    LOG_FILE_SIZE = 3


if not os.path.exists(BaseConfig.LOG_FOLDER):
    os.makedirs(BaseConfig.LOG_FOLDER)