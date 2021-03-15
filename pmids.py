import pandas as pd
from tqdm import tqdm

chemical_disease_file = '../../send/chemicals_diseases_relation.csv'

chemical_disease = pd.read_csv(chemical_disease_file, sep='\t')

# get all the pmids
pmids = set()
for i in tqdm(range(len(chemical_disease))):
    paper_list = chemical_disease.loc[i]['pmids']
    if pd.isnull(paper_list):
        continue
    for pmid in paper_list.split('|'):
        pmids.add(pmid)

pmids = list(pmids)

pmids_pd = pd.DataFrame(pmids, columns=['pmid'])
pmids_pd.to_csv('pmids_list.csv')
