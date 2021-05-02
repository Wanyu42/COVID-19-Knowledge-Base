import sqlite3
import nltk
import pickle

conn = sqlite3.connect('../paper_list.db')
cursor = conn.cursor()
select_sql = '''SELECT PMID, ABSTRACT, TITLE FROM PAPER_LIST'''

cursor.execute(select_sql)

filename = './learning'
f = open(filename, 'wb')
# Get the paper info
for paper in cursor:
    #paper_dict['abstract'] = paper_info[6]
    pmid = paper[0]
    words = nltk.word_tokenize(paper[1])
    abstract = [word.lower() for word in words if word.isalpha()]
    words = nltk.word_tokenize(paper[2])
    title = [word.lower() for word in words if word.isalpha()]
    pickle.dump([pmid, abstract, title], f)

f.close()
conn.close()