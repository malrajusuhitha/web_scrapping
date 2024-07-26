from bs4 import BeautifulSoup
import requests
import json


print('Which Job you\'re looking for: (eg: java,web developer)')
keyword = input('> ')
print('Experience : (eg: 0)')
exp = input('> ')
print('Location : (eg: Hyderabad)')
loc = input('> ')
print(f'Searching for {exp} experience {keyword} jobs in {loc} ...')

def find_jobs():
    r = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords={keyword}&txtLocation={loc}&cboWorkExp1={exp}').text
    soup = BeautifulSoup(r, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    f = open(f'posts/{keyword}_exp{exp}_{loc}.json','w+')
    jsonData = f.read()
    if jsonData == '':
        jsonData = []
    else:
        jsonData = json.loads(jsonData)

    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:

            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            skills = job.find('span', class_='srp-skills').text.strip()
            more_info = job.header.h2.a['href']
            job_dict = {
                "company_name":company_name,
                "required_skills":skills,
                "link":more_info,
                "published":published_date,
            }
            jsonData.append(job_dict)

    f.write(json.dumps(jsonData))
    f.close()
    print(f'Searching for {exp} experience {keyword} jobs in {loc} is completed.')


find_jobs()