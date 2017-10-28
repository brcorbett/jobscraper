# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import hashlib

# Creating pandas DF to hold job data
columns = ["unique_id", "job_title", "company_name"] #["unique_id", "job_title", "company", "location", "summary"]
job_df = pd.DataFrame(columns=columns)

class Indeed:
    def create_unique_id(self, text_ids):
        # Create unique id for job listing with title+company
        m = hashlib.md5()
        text_id = str(text_ids).encode('utf-8')
        string_id = text_id.replace(" ","")
        m.update(string_id)
        unique_id = str(int(m.hexdigest(), 16))[0:12]

        return unique_id

    def extract_data(self, soup):
        # Searching through all the jobs
        for div in soup.find_all(name="div", attrs={"class":"row"}):
            # Creating index for job posting in data frame
            num = (len(job_df) + 1)

            # Empty list for job postings
            job_post = []

            # Adding job title to job_post
            for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
                job_post.append(a["title"])

            # Adding company to job_post
            company = div.find_all(name="span", attrs={"class":"company"})
            if len(company) > 0:
                for b in company:
                    job_post.append(b.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs={"class":"result-link_source"})
                for span in sec_try:
                    job_post.append(span.text.strip())

            # Creating unique id for each posting
            text_ids = [''.join(job_post[:2])]
            unique_id = self.create_unique_id(text_ids)
            print(unique_id)

            if any(job_df.unique_id == unique_id):
                continue
            else:
                job_post.insert(0, unique_id)




            job_df.loc[num] = job_post



        #return(job_df)

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

        #job_df.to_csv("job_listings.csv", encoding='utf-8')

if __name__ == "__main__":
    # Grabbing variables to send in to each scraper
    # jobTitle = raw_input('Enter job title: ')
    # location = raw_input('Enter location: ')

    # Inputs for easy testing (remove when done)
    jobTitle = "software"
    location = "San Diego"

    # Indeed is the first site to scrape
    indeed_scraper = Indeed()
    indeed_scraper.grab_jobs(jobTitle, location)
