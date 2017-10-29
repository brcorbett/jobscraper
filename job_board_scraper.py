# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import hashlib
import re

# Creating pandas DF to hold job data
columns = ["unique_id", "job_title", "company_name", "location", "summary", "job_url", "job_board"]
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
                for span in company:
                    job_post.append(span.text.strip())
            else:
                sec_try = div.find_all(name="span", attrs={"class":"result-link_source"})
                for span in sec_try:
                    job_post.append(span.text.strip())

            # Creating unique id for each posting
            text_ids = [''.join(job_post[:2])]
            unique_id = self.create_unique_id(text_ids)

            # Checking for duplicates in data frame, go to next iteration if dup.
            if any(job_df.unique_id == unique_id):
                continue

            # Insert unique_id in the beginning of job post
            job_post.insert(0, unique_id)

            # Grabbing job location
            location = div.find_all(name="span", attrs={"class":"location"})
            for span in location:
                # Removing numbers and tags
                span_stripped = span.text.strip()
                span_text = re.sub(r'\d+', '', span_stripped)
                job_post.append(span_text)

            # Grabbing summary
            summary = div.find_all(name="span", attrs={"class":"summary"})
            for span in summary:
                job_post.append(span.text.strip())

            # Grabbing url from job posting
            for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
                job_href = a["href"]
                job_url = "https://www.indeed.com"+job_href
                job_post.append(job_url)

            # Adding job board to end of job listing
            job_post.append("Indeed")

            # Add job posting to job data frame
            job_df.loc[num] = job_post

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

        return job_df

class Glassdoor:
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
        for div in soup.find_all(name="article", attrs={"id":"MainCol"}):
            # Creating index for job posting in data frame
            num = (len(job_df) + 1)

            # Empty list for job postings
            job_post = []

            job_listing =  div.find_all(name="i", attrs={"class":"info"})
            for i in job_listing:
                # Adding job title to job_post
                job_post.append(i["data-jobtitle"])
                # Adding company to job_post
                job_post.append(i["data-employer-shortname"])

            # Creating unique id for each posting
            text_ids = [''.join(job_post[:2])]
            unique_id = self.create_unique_id(text_ids)

            # Checking for duplicates in data frame, go to next iteration if dup.
            if any(job_df.unique_id == unique_id):
                continue

            # Insert unique_id in the beginning of job post
            job_post.insert(0, unique_id)



        return job_df


    def grab_jobs(self, jobTitle, location):
        # Glassdoor doesn't accept get requests without a header.
        headers = {	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				    'accept-encoding': 'gzip, deflate, sdch, br',
				    'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
				    'referer': 'https://www.glassdoor.com/',
				    'upgrade-insecure-requests': '1',
				    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
				    'Cache-Control': 'no-cache',
				    'Connection': 'keep-alive'
	                   }

    	location_headers = {
    		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
    		'accept-encoding': 'gzip, deflate, sdch, br',
    		'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
    		'referer': 'https://www.glassdoor.com/',
    		'upgrade-insecure-requests': '1',
    		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
    		'Cache-Control': 'no-cache',
    		'Connection': 'keep-alive'
    	       }
    	data = {
            "term": location,
    		"maxLocationsToReturn": 10
            }

        location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"

        try:
                # Getting location id for search location
                time.sleep(1)
                location_response = requests.post(location_url, headers=location_headers, data=data).json()
                place_id = location_response[0]['locationId']
                job_listing_url = 'https://www.glassdoor.com/Job/jobs.htm'

                data = {
                    'clickSource': 'searchBtn',
    			    'sc.keyword': jobTitle,
    			    'locT': 'C',
    			    'locId': place_id,
    			    'jobType': ''
                }

                if place_id:
                    time.sleep(1)
                    r = requests.post(job_listing_url, headers=headers, data=data)

                    # Convert html_doc with BeautifulSoup
                    soup = BeautifulSoup(r.text, 'html.parser')

                    job_df = self.extract_data(soup)

                    #return job_df

                else:
                    print "Location id is not available"


        except:
                print("Location gathering failed")


if __name__ == "__main__":
    # Grabbing variables to send in to each scraper
    # jobTitle = raw_input('Enter job title: ')
    # location = raw_input('Enter location: ')

    # Inputs for easy testing (remove when done)
    jobTitle = "software"
    location = "San Diego"

    # Indeed is the first site to scrape
    # indeed_scraper = Indeed()
    # job_df = indeed_scraper.grab_jobs(jobTitle, location)

    glass_scraper = Glassdoor()
    glass_scraper.grab_jobs(jobTitle, location)

    #job_df.to_csv("job_listings.csv", encoding='utf-8')
