from config import BaseConfig
from threading import Thread

class EmailOutput(Thread):
    def __init__(self, results):
        Thread.__init__(self)
        self.work = results

    def run(self):
        while True:
            domain, emaillist = self.work.get()
            email = " ".join(emaillist)

            with open(BaseConfig.OUTPUT_FILE,"a") as rf:
                rf.write(f"{domain} {email}\n")

            self.work.task_done()
