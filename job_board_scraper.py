# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Creating pandas DF to hold job data
columns = ["id", "job_title", "company", "location", "summary"]
job_df = pd.DataFrame(columns=columns)

class Indeed:
    def extract_data(self, soup):
        job_post = []

        # Grabbing company name
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            company = div.find_all(name="span", attrs={"class":"company"})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs={"class":"result-link_source"})
                for span in sec_try:
                    companies.append(span.text.strip())

        return(job_df)

    def grab_jobs(self, jobTitle, location):
        # Modify job title & location
        formatted_job_title = jobTitle.replace(" ", "-")
        formatted_loc = location.replace(" ", "-")

        # Specify the url
        job_url = "https://www.indeed.com/q-" + formatted_job_title + "-l-" +\
                   formatted_loc + "-jobs.html"

        # Grabs request from GET request
        r = requests.get(job_url)
        time.sleep(1)

        # Convert html_doc with BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')

        job_df = self.extract_data(soup)

        print(job_df)

if __name__ == "__main__":
    # Grabbing variables to send in to each scraper
    jobTitle = raw_input('Enter job title: ')
    location = raw_input('Enter location: ')

    # Indeed is the first site to scrape
    indeed_scraper = Indeed()
    indeed_scraper.grab_jobs(jobTitle, location)
