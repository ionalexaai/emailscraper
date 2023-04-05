"""Simple Email Scraper against a list of domains"""

import queue
import warnings

from config import BaseConfig
from loggers import logger
from scraper_class import DomainExplorer
from results_class import EmailOutput

# Ignore warnings because of verify=False on SSL certificates
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # Define two queues to work with
    domainqueue = queue.Queue()
    emailsqueue = queue.Queue()

    # pylint: disable=W0511
    # TODO: Add domains to queue inside the context manager and use queue maxsize for efficiency
    with open(BaseConfig.HOSTS_FILE, "r", encoding="utf-8") as domains_file:
        domains = domains_file.read().splitlines()

    for domain in domains:
        domainqueue.put(domain)

    # Start our threads
    for _i in range(BaseConfig.THREADS_NUMBER):
        t = DomainExplorer(domainqueue, emailsqueue)
        t.daemon = True
        t.start()

    logger.info(f"Started {BaseConfig.THREADS_NUMBER} Threads")

    # Start our collector thread
    results_thread = EmailOutput(emailsqueue)
    results_thread.daemon = True
    results_thread.start()

    # Gracefully join our queues so that our threads can exit
    domainqueue.join()
    logger.info("Domains finished processing")
    emailsqueue.join()
    logger.info("Collector finished processing")
