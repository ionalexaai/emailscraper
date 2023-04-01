from bs4 import BeautifulSoup
import requests
from threading import Thread
import queue
import re
from loggers import logger

class DomainExplorer(Thread):
    def __init__(self, workerqueue, resultsqueue):
        
        Thread.__init__(self)
        self.work = workerqueue
        self.results = resultsqueue
        self.r = requests.Session()
        self.timeout = 10
        self.r.headers.update({"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"})
        self.pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
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
        logger.info(self.domain + " " + str(found_emails))
            


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
