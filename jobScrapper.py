import requests
from bs4 import BeautifulSoup
import csv

unfamiliar_skills = input('Enter One unfamiliar skills')
print(f"Here we are now filtering;{unfamiliar_skills}")
# info = {}

outfile = open('jobs.csv', 'w', newline='')
writer = csv.writer(outfile)
writer.writerow(["Company Name", "Skills Set",
                "Information Link", "Description", "Posted Time"])


def search_job():
    # sequence = 1
    startPage = 1
    for i in range(1, 11):
        print(f"Loop count:{i}")
        url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=I&sequence=' + \
            str(i)+'&startPage='+str(startPage)

        if i % 10 == 0:
            startPage = startPage+10
        # url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=I&sequence=1&startPage=1'
        # status = requests.get(url)
        text = requests.get(url).content
        soup = BeautifulSoup(text, 'lxml')
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        # print(jobs)
        for job in jobs:
            date = job.find('span', class_="sim-posted").span.text
            if 'Posted' in date:
                company_name = job.find(
                    'h3', class_="joblist-comp-name").text.replace(' ', '')
                print(company_name)
                skills = job.find(
                    'span', class_="srp-skills").text.replace(' ', '')
                print(skills)
                # description_link = job.find(
                #     'header', class_="clearfix").h2.a["href"]
                description_link = job.header.h2.a["href"]
                # print(description_link)
                if unfamiliar_skills not in skills:
                    more_info = requests.get(description_link).content
                    info_soup = BeautifulSoup(more_info, 'lxml')
                    description = info_soup.find(
                        'div', class_="jd-desc job-description-main").text.replace(' ', '')

                    writer.writerow([company_name.strip(), skills.strip(
                    ), description_link.strip(), description.strip(), date.strip()])
                    # print(f"Company Name:{company_name.strip()}")
                    # print(f"Skills set:{skills.strip()}")
                    # print(f"Information:{description_link.strip()}")
                    # print(f"Description: {description.strip()}")
    outfile.close()


search_job()

# print(len(info))

# if __name__ == "__main___":
#     while True:
#         search_job()
