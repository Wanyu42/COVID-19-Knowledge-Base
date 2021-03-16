import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent import futures

'''
Use threading to speed up the webpage crawling
'''

pmids_df = pd.read_csv('pmids_list.csv')
pmids_list = list(pmids_df['pmid'])

root = 'http://www.ncbi.nlm.nih.gov/pubmed/'
doi_prefix = 'https://doi.org/'

paper_list = []

#pmids_list = pmids_list[:20]

def get_doi(pmid):
    response = requests.get(root+str(pmid))
    if response.status_code == 200:
        #soup = BeautifulSoup(response.text, "html.parser")
        #return [pmid,doi_prefix + soup.find_all(attrs={"name": "citation_doi"})[0]['content']]
        return [pmid, response.text]
    else:
        #return [pmid, None]
        return [pmid, None]

processes = []
with futures.ThreadPoolExecutor(max_workers=8) as executor:
    for pmid in pmids_list:
        processes.append(executor.submit(get_doi, pmid))
for task in futures.as_completed(processes):
    pmid, html_text = task.result()
    # html_text == None means the web requests return Error
    if html_text == None:
        continue

    soup = BeautifulSoup(html_text, "html.parser")
    doi_suffix = soup.find_all(attrs={"name": "citation_doi"})[0]['content']
    # '' means there is no doi
    if(doi_suffix == ''):
        doi = None
    else:
        doi = doi_prefix + doi_suffix

    title = soup.find(attrs={'name': 'citation_title'})['content']
    authors = soup.find(attrs={'name': 'citation_authors'})['content']
    date = soup.find('meta', attrs={'name': 'citation_date'})['content']

    cited_list = soup.find_all('a', class_='docsum-title', attrs={'data-ga-category': 'cited_by'})
    cited_pmid = [cited['data-ga-action'] for cited in cited_list]

    paper_list.append([pmid,doi,title,authors,date,('|').join(cited_pmid)])

## Paper_list contains [pmid,doi,title,authors,date,cited_pmid] fields

paper_pd = pd.DataFrame(paper_list,columns=['pmid','doi','title','authors','date', 'cited_pmid'])
paper_pd.to_csv('paper_list.csv')

