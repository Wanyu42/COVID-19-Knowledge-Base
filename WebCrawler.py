import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

root = 'http://www.ncbi.nlm.nih.gov/pubmed/'
pmids_df = pd.read_csv('hahh.csv')

doi_prefix = 'https://doi.org/'
doi_list = []
for i in tqdm(range(len(pmids_df))):
    response = requests.get(root+str(pmids_df.loc[i]['pmid']))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        doi_list.append(doi_prefix + soup.find_all(attrs={"name": "citation_doi"})[0]['content'])
    else:
        doi_list.append(None)

pmids_df['doi'] = doi_list

pmids_df.head(10)
pmids_df.to_csv('pmid_doi.csv')
