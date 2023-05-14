import requests
from bs4 import BeautifulSoup
import pandas as pd

link = requests.get('https://itc.gymkhana.iitb.ac.in/wncc/soc/').text
soup = BeautifulSoup(link, 'lxml')

column_headers= ['Project', 'Mentor', 'Mentee', 'Project Description']
dataframe = pd.DataFrame(columns=column_headers)

projects = soup.find_all('a')

for project in projects:
    try:
        plink = requests.get('https://itc.gymkhana.iitb.ac.in'+project['href']).text
    except:
        plink='NAN'
    if 'project' in plink:

        soup2 = BeautifulSoup(plink, 'lxml')
        actual_project = soup2.find('div', class_='col-sm-10 col-md-8')
        if actual_project is not None:
            name = actual_project.find('h2',class_='display1 m-3 p-3 text-center project-title').text
            mentors = actual_project.find_all('p', class_='lead')
            i=0
            mentorlist = ''
            for mentor in mentors:
                if mentor.text[0].isalpha():
                    i=i+1
                    mentorlist += mentor.text + ', '
            mentee = actual_project.find_all('p', class_='lead')[i].text
            desc = actual_project.find('p', class_='display3 project-desc')
            if not desc:
                desc = actual_project.find('p', class_='display3')
            

            if (name!=''):
                dataframe = dataframe._append(
                    pd.Series([
                        name,
                        mentorlist,
                        mentee,
                        desc.text
                    ],
                    index = column_headers),
                    ignore_index = True)


dataframe.to_excel('SoC.xlsx')
print('DataFrame is written to Excel File successfully.')
    