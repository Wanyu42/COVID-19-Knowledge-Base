import pickle
import nltk
from nltk.corpus import stopwords
import numpy as np
import operator

def read_abstract_title():
    pickle_file = open("learning", "rb")
    objects = []
    while True:
        try:
            objects.append(pickle.load(pickle_file))
        except EOFError:
            break
    pickle_file.close()

    return objects

dataset = read_abstract_title()
stop_words = set(stopwords.words('english'))

long_list = []
for sent in dataset:
    for word in sent[1]+sent[2]:
        long_list.append(word)

fdist1 = nltk.FreqDist(long_list)
filtered_words = list(word for word, freq in fdist1.items() if freq > 5)
filtered_words = [word for word in filtered_words if word not in stop_words]

del long_list

word2idx = {'_PAD_':0}
for word in filtered_words:
    word2idx[word] = len(word2idx)

train_filename = './train'
val_filename = './val'
vocab_filename = './vocab_dict'

max_abstract_length = 256
max_title_length = 16

total_doc_num = range(len(dataset))
np.random.seed(0)
paper_ids = np.random.permutation(total_doc_num)

train_size = 50000
val_size = 10000

train_set = operator.itemgetter(*paper_ids[:train_size])(dataset)
val_set = operator.itemgetter(*paper_ids[train_size:val_size+train_size])(dataset)

f = open(train_filename, 'wb')
# Get the paper info
for paper in train_set:
    pmid = paper[0]
    abstract = [word for word in paper[1] if word in filtered_words]
    if len(abstract) >= max_abstract_length:
        abstract = abstract[:max_abstract_length]
    else:
        pad_num = max_abstract_length - len(abstract)
        abstract.extend(pad_num*['_PAD_'])
    title = [word for word in paper[2] if word in filtered_words]
    if len(title) >= max_title_length:
        title = title[:max_title_length]
    else:
        pad_num = max_title_length - len(title)
        title.extend(pad_num*['_PAD_'])
    pickle.dump([pmid, abstract, title], f)
f.close()

f = open(val_filename, 'wb')
for paper in val_set:
    pmid = paper[0]
    abstract = [word for word in paper[1] if word in filtered_words]
    if len(abstract) >= max_abstract_length:
        abstract = abstract[:max_abstract_length]
    else:
        pad_num = max_abstract_length - len(abstract)
        abstract.extend(pad_num*['_PAD_'])
    title = [word for word in paper[2] if word in filtered_words]
    if len(title) >= max_title_length:
        title = title[:max_title_length]
    else:
        pad_num = max_title_length - len(title)
        title.extend(pad_num*['_PAD_'])
    pickle.dump([pmid, abstract, title], f)
f.close()

f = open(vocab_filename, 'wb')
pickle.dump(word2idx, f)
f.close()