import queue
import warnings

from config import BaseConfig
from loggers import logger
from scraper_class import DomainExplorer

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    domainqueue = queue.Queue()
    emailsqueue = queue.Queue()
    workers = []

    with open(BaseConfig.HOSTS_FILE,"r") as domains_file:
        domains = domains_file.read().splitlines()

    for domain in domains:
        domainqueue.put(domain)

    for _i in range(BaseConfig.THREADS_NUMBER):
        t = DomainExplorer(domainqueue, emailsqueue)
        t.daemon = True
        t.start()
        workers.append(t)

    while True:
        domain, emaillist = emailsqueue.get()
        email = " ".join(emaillist)
        with open(BaseConfig.OUTPUT_FILE,"a") as rf:
            rf.write(f"{domain} {email}\n")


    for worker in workers:
        worker.join()
