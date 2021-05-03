from train import *
import numpy as np


# (batch_num, batch_size, sentence_length) 256 or 16
# return: abstract_vect (batch_num, batch_size, 256)
#         title_vect (batch_num, batch_size, 16)
#         label (batch_num, batch_size)

def eval_data_prepare(dataset, batch_size, word2idx):
    data_size = len(dataset)
    batch_num = data_size // batch_size

    if (data_size % batch_size != 0):
        pad_num = (data_size // batch_size + 1) * batch_size - data_size
        data_pad = pad_num * [[-1, 256 * ['_PAD_'], 16 * ['_PAD_']]]
        dataset.extend(data_pad)
        batch_num += 1

    abstract_vect = list()
    title_vect = list()
    pmid_vect = list()

    for i in range(batch_num):
        batch_abstract_vect = list()
        batch_title_vect = list()
        batch_pmid = list()

        batch_data = dataset[i * batch_size: i * batch_size + batch_size]
        for j in range(batch_size):
            batch_abstract_vect.append(sent_to_vect(batch_data[j][1], word2idx))
            batch_title_vect.append(sent_to_vect(batch_data[j][2], word2idx))

            batch_pmid.append(torch.tensor(batch_data[j][0], dtype=torch.int))

        # batch_abstract_vect (batch_size, sentence_length)
        abstract_vect.append(torch.vstack(batch_abstract_vect))
        title_vect.append(torch.vstack(batch_title_vect))
        pmid_vect.append(torch.vstack(batch_pmid))

    abstract_vect = torch.stack(abstract_vect)
    title_vect = torch.stack(title_vect)
    pmid_vect = torch.stack(pmid_vect)
    return pmid_vect, abstract_vect, title_vect


if __name__ == "__main__":
    torch.manual_seed(0)
    whole_data = read_abstract_title('whole')

    word2idx = read_abstract_title('vocab_dict')
    word2idx = word2idx[0]

    glove = pd.read_csv('glove.6B.50d.txt', sep=" ", quoting=3, header=None, index_col=0)
    glove_embedding = {key: val.values for key, val in glove.T.items()}

    ## pre-trained word embedding
    embedding_matrix = create_embedding_matrix(word2idx, glove_embedding, dimension=50)

    del glove
    del glove_embedding

    vocab_size = embedding_matrix.shape[0]
    embedding_dim = embedding_matrix.shape[1]

    ##############################################################
    ##############################################################
    ## Build the model
    batch_size = 50
    hidden_size = 64
    real_size = len(whole_data)

    pmid, abstract, title = eval_data_prepare(whole_data, batch_size, word2idx)

    abstract_len = abstract.shape[2]
    title_len = title.shape[2]

    ##########################################################
    ################## Load the model ##############################
    PATH = 'tut_mod-model.pt'
    rr = Representation(vocab_size, embedding_dim, embedding_matrix,
                        hidden_size, batch_size, abstract_len, title_len)
    rr.load_state_dict(torch.load(PATH))

    ###############################################################
    ################## Learn Representation #######################
    batch_num = len(whole_data) // batch_size
    pmid_list = list()
    whole_represent = list()
    with torch.no_grad():
        for k in range(batch_num):
            represent = rr(abstract[k], title[k])
            whole_represent.append(represent)
            pmid_list.append(pmid[k].squeeze())

        pmid_list = torch.cat(pmid_list)
        whole_represent = torch.vstack(whole_represent)

    whole_represent = whole_represent[:real_size, :]
    pmid_list = pmid_list[:real_size]

    repre_dict = dict(zip(pmid_list.numpy(), whole_represent.numpy()))

    f = open('repre_dict', 'wb')
    pickle.dump(repre_dict, f)
    f.close()

