# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_company_from_result(soup):
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link_source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)

def grab_job_listings(jobTitle, location):
    # Modify job title & location
    formatted_job_title = jobTitle.replace(" ", "-")
    formatted_loc = location.replace(" ", "-")

    # Specify the url
    job_url = "https://www.indeed.com/q-" + formatted_job_title + "-l-" +\
               formatted_loc + "-jobs.html"

    # Grabs request from GET request
    r = requests.get(job_url)

    # Convert html_doc with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    companies = extract_company_from_result(soup)

    print(companies)

jobTitle = raw_input('Enter job title: ')
location = raw_input('Enter location: ')

grab_job_listings(jobTitle, location)
