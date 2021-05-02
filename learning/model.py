import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):
    def __init__(self, vocab_size, embedding_dim,embedding_matrix,hidden_size, batch_size, seq_len):
        super(Encoder, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.seq_len = seq_len

        self.embedding = nn.Embedding(num_embeddings=vocab_size,
                                      embedding_dim=embedding_dim, padding_idx=0)
        self.embedding.weight = nn.Parameter(torch.tensor(embedding_matrix, dtype=torch.float32))

        self.lstm = nn.LSTM(embedding_dim, hidden_size // 2,
                            num_layers=1, bidirectional=True, batch_first=True)
        self.linear = nn.Linear(hidden_size, hidden_size)

    def forward(self, sent):
        """
        the returned repre has size (batch_size, hidden_dim), each row is a sentence
        """
        embeds = self.embedding(sent).view(self.batch_size, self.seq_len, -1)
        _, (hn, cn) = self.lstm(embeds)
        repre = self.linear(hn.view(self.batch_size, -1))
        return repre


class Model(nn.Module):
    def __init__(self, vocab_size, embedding_dim, embedding_matrix, hidden_size, batch_size,
                 seq_len_abstract, seq_len_title):
        super(Model, self).__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.seq_len_abstract = seq_len_abstract
        self.seq_len_title = seq_len_title

        self.abstractEnc = Encoder(vocab_size, embedding_dim, embedding_matrix, hidden_size,
                                   batch_size, seq_len_abstract)

        self.titleEnc = Encoder(vocab_size, embedding_dim, embedding_matrix, hidden_size,
                                batch_size, seq_len_title)

        #self.secondfinalLinear = nn.Linear(2*hidden_size, 2*hidden_size)
        self.finalLinear = nn.Linear(2 * hidden_size, 1)

    def forward(self, abstract, title):
        """
        abstract is of size (batch_size, sentence_length = 256)
        title is of sie (batch_szie, sentence_length=16)
        """
        abstract_vect = self.abstractEnc(abstract)
        title_vect = self.titleEnc(title)
        represent = torch.hstack((abstract_vect, title_vect))
        #represent = self.secondfinalLinear(F.relu(represent))
        logits = self.finalLinear(F.relu(represent))
        return logits
