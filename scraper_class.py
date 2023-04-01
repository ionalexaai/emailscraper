from bs4 import BeautifulSoup
import requests
from threading import Thread
import queue
import re
from loggers import logger
from config import BaseConfig

class DomainExplorer(Thread):
    def __init__(self, workerqueue, resultsqueue):
        
        Thread.__init__(self)
        self.work = workerqueue
        self.results = resultsqueue
        self.r = requests.Session()
        self.timeout = BaseConfig.REQUEST_TIMEOUT
        self.r.headers.update(BaseConfig.HEADERS)
        self.pattern = BaseConfig.EMAIL_PATTERN
        logger.info("Thread Started")


    def run(self):
        while True:
            try:
                self.domain = self.work.get()
                self.main()
                self.work.task_done()
            except Exception as e:
                logger.error(str(e))

    def main(self):

        self.url = self.domain if self.domain.startswith("http") else "http://"+self.domain

        self.src = self.get_page_source()
        self.links = self.get_page_links()

        if self.url not in self.links:
            self.links.append(self.url)

        found_emails = self.get_emails()

        self.results.put((self.domain, found_emails))
        #logger.info(self.domain + " " + str(found_emails))
            


    def get_page_source(self):

        response = self.r.get(self.url, timeout=self.timeout, verify=False)

        return response.text

    def get_page_links(self):

        links = []
        self.soup = BeautifulSoup(self.src, 'html.parser')
        if self.soup:

            for link in self.soup.find_all('a'):
                url = link.get('href')
                if self.domain in str(url) and url.startswith("http"):
                    links.append(link.get('href'))
                    #print(link.get('href'))

        return list(set(links))

    def get_emails(self):
        emails = []

        for link in self.links:
            try:
                response = self.r.get(link, timeout = self.timeout, verify=False)
                #print(link)
                emails2 = re.findall(self.pattern, response.text)
                for email in emails2:
                    if email not in emails and "/" not in email and "\\" not in email :
                        emails.append(email)
            except Exception as e:
                logger.error(f"{link} Didn't Process because: {e}")
                return list(set(emails))

        return list(set(emails))
