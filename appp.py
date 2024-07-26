from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import mysql.connector

app = Flask(__name__)


# Database connection (if needed)
def get_db_connection():
    conn = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_user",
        password="your_mysql_password",
        database="your_database"
    )
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        role = request.form['role']
        location = request.form['location']
        experience = request.form['experience']

        # Debug prints
        print(f"Role: {role}")
        print(f"Location: {location}")
        print(f"Experience: {experience}")

        jobs = scrape_jobs(role, location, experience)

        # More debug prints
        print(f"Jobs found: {len(jobs)}")
        for job in jobs:
            print(job)

        # Message for no jobs found
        if len(jobs) == 0:
            message = "No jobs found."
        else:
            message = None

        return render_template('index.html', jobs=jobs, message=message)
    return render_template('index.html', jobs=[], message=None)


def scrape_jobs(role, location, experience):
    # Modify search URL to include role and location
    search_url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={role.replace(' ', '+')}+{experience.replace(' ', '+')}&txtLocation={location.replace(' ', '+')}"
    print(f"Scraping URL: {search_url}")  # Debug print
    response = requests.get(search_url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data from {search_url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for li in soup.find_all(name="li", attrs={"class": "clearfix job-bx wht-shd-bx"}):
        title_elem = li.find(name="header", attrs={"class": "clearfix"})
        company_elem = li.find(name="h3", attrs={"class": "joblist-comp-name"})
        location_elem = li.find(name="ul", attrs={"class": "top-jd-dtl clearfix"})
        summary_elem = li.find(name="ul", attrs={"class": "list-job-dtl clearfix"})

        if title_elem and company_elem and location_elem and summary_elem:
            title = title_elem.a.text.strip()
            company = company_elem.text.strip()
            location = location_elem.find("span").text.strip()
            summary = summary_elem.text.strip()
            jobs.append({"title": title, "company": company, "location": location, "summary": summary})
        else:
            print("Missing job information, skipping this entry.")  # Debug print

    return jobs


if __name__ == '__main__':
    app.run(debug=True)