import logging
import inspect
from logging.handlers import RotatingFileHandler


class StreamAndMongoLogger:
    def __init__(self, name, log_file, max_bytes=10485760, backup_count=5, level=logging.DEBUG, mongo_uri=None, mongo_col="logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.log_file = log_file
        
        formatter = logging.Formatter('%(asctime)s-[%(name)s] - %(levelname)s - [%(source_file)s:%(line_number)d] - %(message)s')
        
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter('[%(name)s:%(levelname)s]-[%(source_file)s:%(line_number)d] - %(message)s'))
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.propagate = False
        
        if mongo_uri:
            self.client = MongoClient(mongo_uri)
            self.db = self.client['logs']
            self.logs = self.db[mongo_col]
            mongo_handler = MongoDBHandler(self.logs)
            mongo_handler.setLevel(level)
            mongo_handler.setFormatter(formatter)
            self.logger.addHandler(mongo_handler)
        
    def info(self, message):
        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        lineno = frame.lineno        
        self.logger.info(message, extra={'source_file': filename, 'line_number': lineno})
        
    def debug(self, message):
        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        lineno = frame.lineno          
        self.logger.debug(message, extra={'source_file': filename, 'line_number': lineno})
        
    def warning(self, message):
        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        lineno = frame.lineno          
        self.logger.warning(message, extra={'source_file': filename, 'line_number': lineno})
        
    def error(self, message):
        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        lineno = frame.lineno          
        self.logger.error(message, extra={'source_file': filename, 'line_number': lineno})
        
    def critical(self, message):
        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        lineno = frame.lineno          
        self.logger.critical(message, extra={'source_file': filename, 'line_number': lineno})

class MongoDBHandler(logging.Handler):
    def __init__(self, collection):
        logging.Handler.__init__(self)
        self.collection = collection
        
    def emit(self, record):
        # Format the log message
        message = self.format(record)
        
        # Insert the log message into the MongoDB collection
        self.collection.insert_one({'message': message})

