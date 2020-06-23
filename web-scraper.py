import requests
from bs4 import BeautifulSoup
import csv

from_date = '1990-01-01'
to_date = '2017-11-01'
topic = 'computer science'

if (' ' in topic):
    new_topic = topic.replace(' ', '+')
    URL = f'https://arxiv.org/search/?query={new_topic}&searchtype=all&date-year=&date-filter_by=date_range&date-from_date={from_date}&date-to_date={to_date}&date-date_type=submitted_date&order=-submitted_date'
else: URL = f'https://arxiv.org/search/?query={topic}&searchtype=all&date-year=&date-filter_by=date_range&date-from_date={from_date}&date-to_date={to_date}&date-date_type=submitted_date&order=-submitted_date'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

container = soup.find('main', class_='container')
container = soup.find('ol', class_='breathe-horizontal')
results = container.find_all('li', class_='arxiv-result')


results_list = []
for result in results:
    title=result.find('p', class_='title').text
    authors=result.find('p', class_='authors').text.replace('Authors:', '')
    first_author=authors.split(', ')[0]
    last_author=authors.split(', ')[-1]
    summary=result.find('p', class_='abstract').text.replace('△ Less', ' ').replace('▽ More', ' ').replace('Abstract:', ' ')
    pdf=result.find('div', class_='is-marginless').find('p', class_='list-title').find('span').find('a', text='pdf', href=True)
    
    paper = {
        "Title": title.replace('\n', ' ').strip(), 
        "First Author": first_author.replace('\n', ' ').strip(), 
        "Last Author": last_author.replace('\n', ' ').strip(), 
        "Summary": summary.replace('\n', ' ').strip(),
        "PDF": pdf['href'] if pdf else 'N/A'
    }

    results_list.append(paper)

with open('papers.csv', 'w') as out_file:
    headers = [
        "Title",
        "First Author",
        "Last Author",
        "Summary",
        "PDF"
    ]
    writer = csv.DictWriter(out_file, lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    i = 0
    for paper in results_list:
        writer.writerow(paper)