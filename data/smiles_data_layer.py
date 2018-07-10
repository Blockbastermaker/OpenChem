# TODO: packed variable length sequence

import numpy as np

from torch.utils.data import Dataset

from data.utils import read_smiles_property_file
from data.utils import sanitize_smiles, pad_sequences, seq2tensor
from data.utils import tokenize


class SmilesDataset(Dataset):
    def __init__(self, filename, cols_to_read, delimiter=',', tokens=None,
                 pad=True):
        super(SmilesDataset, self).__init__()
        data, target = read_smiles_property_file(filename, delimiter,
                                                 cols_to_read)
        clean_smiles, clean_idx = sanitize_smiles(data)
        target = np.array(target)
        self.target = target[clean_idx]
        if pad:
            clean_smiles = pad_sequences(clean_smiles)
        self.tokens, self.token2idx, self.num_tokens = tokenize(clean_smiles,
                                                                tokens)
        clean_smiles = seq2tensor(clean_smiles, self.tokens)
        self.data = clean_smiles

    def __len__(self):
        return len(self.target)

    def __getitem__(self, index):
        sample = {'tokenized_smiles': self.data[index],
                  'labels': self.target[index]}
        return sample