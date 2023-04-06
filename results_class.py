"""Email Collector class"""
from threading import Thread
from config import BaseConfig

class EmailOutput(Thread):
    """Email Collector Class"""
    def __init__(self, results):
        Thread.__init__(self)
        self.work = results

    def run(self):
        while True:
            domain, emaillist = self.work.get()
            email = " ".join(emaillist)

            with open(BaseConfig.OUTPUT_FILE, "a", encoding="utf-8") as results_file:
                results_file.write(f"{domain} {email}\n")

            self.work.task_done()
