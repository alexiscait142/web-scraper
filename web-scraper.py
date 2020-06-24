import requests
from bs4 import BeautifulSoup
import csv

from_date = '2000-01-01'
to_date = '2020-11-01'
topic = 'math'

if (' ' in topic):
    new_topic = topic.replace(' ', '+')
    URL = f'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={new_topic}&terms-0-field=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={from_date}&date-to_date={to_date}&date-date_type=submitted_date&abstracts=show&size=50&order=-submitted_date'
else: URL = f'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={topic}&terms-0-field=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={from_date}&date-to_date={to_date}&date-date_type=submitted_date&abstracts=show&size=50&order=-submitted_date'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

errors = []
error = soup.find('div', class_='is-warning')
container = soup.find('ol', class_='breathe-horizontal')

if error:
    error_message = soup.find('div', class_='box').find_all('div', class_='is-warning')
    for err in error_message:
        errors.append({"Error Message": err.text.replace('\n', ' ')})
    with open('Papers.csv', 'w') as out_file:
        headers = [
            "Error Message"
        ]
        writer = csv.DictWriter(out_file, fieldnames=headers)
        writer.writeheader()
        for err in errors:
            writer.writerow(err)
    print("There was a problem with your request. See the 'Papers.csv' for details.")
elif container:
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

    with open('Papers.csv', 'w') as out_file:
        headers = [
            'Topic',
            'Date Range',
            "Title",
            "First Author",
            "Last Author",
            "Summary",
            "PDF"
        ]
        writer = csv.DictWriter(out_file, fieldnames=headers)
        writer.writeheader()
        writer.writerow({"Topic": topic, "Date Range": f'{from_date} - {to_date}'})
        for paper in results_list:
            writer.writerow(paper)
    print("Success! See the 'Papers.csv' for details.")