import pickle
import numpy as np
import pandas as pd
import torch.optim as optim

from model import *


def read_abstract_title(filename):
    pickle_file = open(filename, "rb")
    objects = []
    while True:
        try:
            objects.append(pickle.load(pickle_file))
        except EOFError:
            break
    pickle_file.close()

    return objects


def create_embedding_matrix(word_index, embedding_dict, dimension):
    embedding_matrix = np.zeros((len(word_index) + 1, dimension))

    for word, index in word_index.items():
        if word in embedding_dict:
            embedding_matrix[index] = embedding_dict[word]
    return embedding_matrix


def sent_to_vect(sent, word2idx):
    sent_vect = [word2idx[word] for word in sent]
    return torch.tensor(sent_vect, dtype=torch.int)


# (batch_num, batch_size, sentence_length) 256 or 16
# return: abstract_vect (batch_num, batch_size, 256)
#         title_vect (batch_num, batch_size, 16)
#         label (batch_num, batch_size)
def prepare_data(dataset, batch_size, pertube_prob, word2idx):
    data_size = len(dataset)
    batch_num = data_size // batch_size
    abstract_vect = list()
    title_vect = list()
    label = list()
    idx = torch.tensor(range(batch_size))

    for i in range(batch_num):
        batch_abstract_vect = list()
        batch_title_vect = list()
        # mask with true means the label is 0 (permuted)
        mask = torch.rand(batch_size) > pertube_prob
        permute = torch.remainder(mask * (torch.randint(1, batch_size - 1, (batch_size,)))
                                  + idx, batch_size)

        batch_data = dataset[i * batch_size: i * batch_size + batch_size]
        batch_label = 1 * (mask == False)

        for j in range(batch_size):
            batch_abstract_vect.append(sent_to_vect(batch_data[j][1], word2idx))
            batch_title_vect.append(sent_to_vect(batch_data[permute[j].item()][2], word2idx))

        # batch_abstract_vect (batch_size, sentence_length)
        abstract_vect.append(torch.vstack(batch_abstract_vect))
        title_vect.append(torch.vstack(batch_title_vect))
        label.append(batch_label)

    abstract_vect = torch.stack(abstract_vect)
    title_vect = torch.stack(title_vect)
    label = torch.stack(label).float()

    return abstract_vect, title_vect, label


if __name__ == "__main__":
    torch.manual_seed(0)
    train_data = read_abstract_title('train')
    val_data = read_abstract_title('val')

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

    train_abstract, train_title, train_label = prepare_data(train_data, batch_size, 0.5, word2idx)
    val_abstract, val_title, val_label = prepare_data(val_data, batch_size, 0.5, word2idx)

    abstract_len = train_abstract.shape[2]
    title_len = train_title.shape[2]

    mm = Model(vocab_size, embedding_dim, embedding_matrix,
               hidden_size, batch_size, abstract_len, title_len)

    optimizer = optim.Adam(mm.parameters())
    loss_fn = nn.BCEWithLogitsLoss()

    ##########################################################
    ################## Training ##############################
    N_EPOCHS = 5
    best_val_acc = float('-inf')
    batch_num = train_label.shape[0]
    val_num = val_label.shape[0]

    for epoch in range(N_EPOCHS):
        # Train process
        running_loss = 0.0
        mm.train()
        for i in range(batch_num):
            # zero the gradients
            mm.zero_grad()
            # compute the logits
            logits = mm(train_abstract[i], train_title[i])
            # binary cross entropy loss
            loss = loss_fn(logits.squeeze(), train_label[i])
            # backpropagate
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 200 == 199:  # print every 200 mini-batches
                print('[%d, %5d] loss: %.5f' %
                      (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0

        # evaluate every epoch
        mm.eval()
        with torch.no_grad():
            acc = 0.0
            for k in range(val_num):
                logits = mm(val_abstract[k], val_title[k])
                preds = 1 * (logits > 0.0)
                acc += (preds.squeeze() == val_label[k]).float().sum()
            acc /= (batch_size * val_num)
            print('Epoch %d, acc: %5f' % (epoch + 1, acc))

            if acc > best_val_acc:
                best_valid_loss = acc
                torch.save(mm.state_dict(), 'tut_mod-model.pt')
