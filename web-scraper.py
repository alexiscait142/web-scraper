import requests
from bs4 import BeautifulSoup
import csv

from_date = '2019-01-01'
to_date = '2020-06-22'

URL = 'https://arxiv.org/search/?query=computer+science&searchtype=all&date-year=&date-filter_by=date_range&date-from_date={from_date}&date-to_date={to_date}&date-date_type=submitted_date&order=-submitted_date'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

container = soup.find('ol', class_='breathe-horizontal') # get container that has results
results = container.find_all('li', class_='arxiv-result') # get each result li

titles = []
first_authors = []
last_authors = []
summaries = []
pdfs = []

def add_to_list(column, string):
    column.append(string.replace('\n', ' ').strip())

for result in results:
    title=result.find('p', class_='title').text # get title
    authors=result.find('p', class_='authors').text.replace('Authors:', '') # get all authors
    first_author=authors.split(', ')[0] # get first author
    last_author=authors.split(', ')[-1] # get last author
    summary=result.find('p', class_='abstract').text.replace('△ Less', ' ').replace('▽ More', ' ').replace('Abstract:', ' ') # get summary/abstract
    pdf=result.find('div', class_='is-marginless').find('p', class_='list-title').find('span').find('a', text='pdf')['href'] # get pdf link
    add_to_list(titles, title)
    add_to_list(first_authors, first_author)
    add_to_list(last_authors, last_author)
    add_to_list(summaries, summary)
    add_to_list(pdfs, pdf)

data = {}
i = 0
while i < len(titles):
    data[titles[i]] = {'First Author': first_authors[i], 'Last Author': last_authors[i], 'Summary': summaries[i], 'PDF': pdfs[i]}
    i += 1

# data[titles[0]] = {'First Author': first_authors[0], 'Last Author': last_authors[0], 'Summary': summaries[0], 'PDF': pdfs[0]}

print(data)

# with open('papers.csv', 'w') as out_file:
#     headers = [
#         "Title",
#         "First Author",
#         "Last Author",
#         "Summary",
#         "PDF Link"
#     ]
#     writer = csv.DictWriter(out_file, headers)
#     writer.writeheader()