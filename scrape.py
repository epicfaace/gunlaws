from bs4 import BeautifulSoup
import requests
import json
import requests_cache
import concurrent.futures

# Enable cache
requests_cache.install_cache('cache_name', expire_after=3600)

results = []

def scrape_page(page):
    response = requests.get(f"https://firearmslaw.duke.edu/repository/search-results/?sf_paged={page}")
    print(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all('a', {'class': 'read'})
    hrefs = [element.get('href') for element in elements]
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for href in hrefs:
            try:
                output = scrape_href(href)
                if output:
                    results.append(output)
            except Exception as e:
                print(href)
                raise e
            # futures.append(executor.submit(scrape_href, href))
        # for future in concurrent.futures.as_completed(futures):
            # results.append(future.result())
    return results

def scrape_href(href):
    if not href.startswith('https://firearmslaw.duke.edu'): return
    response = requests.get(href)

    soup = BeautifulSoup(response.content, 'html.parser')

    data = {'url': href}

    # Get the title
    title = soup.find('h1').text
    data['title'] = title

    # Get the subject(s)
    subjects = []
    subject_tags = soup.find_all('div', {'class': 'col-lg-6 col-md-6 col-sm-12 col-xs-12p'})[0].find('ul').find_all('a')
    for tag in subject_tags:
        subjects.append(tag.text)
    data['subjects'] = subjects

    # Get the jurisdiction(s)
    jurisdictions = []
    ul = soup.find_all('div', {'class': 'col-lg-3 col-md-3 col-sm-3 col-xs-12'})[0].find('ul')
    jurisdiction_tags = ul.find_all('a') if ul else []
    for tag in jurisdiction_tags:
        jurisdictions.append(tag.text)
    data['jurisdictions'] = jurisdictions

    # Get the year(s)
    p = soup.find_all('div', {'class': 'col-lg-3 col-md-3 col-sm-3 col-xs-12'})[1].find('p')
    year = p.text if p else None
    data['year'] = year

    # Get the text
    text = soup.find_all('div', {'class': 'col-lg-12 col-md-12 col-sm-12 col-xs-12'})[1].find_all('p')
    text = [p.text for p in text]
    data['text'] = text
    return data

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    futures = []
    for page in range(1, 70):
        scrape_page(page)
        # futures.append(executor.submit(scrape_page, page))
    # for future in concurrent.futures.as_completed(futures):
        # results.extend(future.result())

with open("output.json", "w+") as file:
    json.dump(results, file, indent=4)