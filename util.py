import os
import torch
import pickle as pickle

def load(dirname):
    preproc_f = os.path.join(dirname, "preproc.bin")
    with open(preproc_f, 'r') as fid:
        preproc = pickle.load(fid)
    return preproc

def save(preproc, dirname):
    preproc_f = os.path.join(dirname, "preproc.bin")
    with open(preproc_f, 'wb') as fid:
        pickle.dump(preproc, fid)

def one_hot(label, depth=12):
    # print(label.shape[0])
    # print(depth)
    # print(type(label))
    # print(label.shape[0])
    # label = torch.tensor(label)
    out = torch.zeros(label.shape[0], depth)
    idx = torch.LongTensor(label).view(-1, 1)
    out.scatter_(dim=1, index=idx, value=1)
    return out


# if __name__ == '__main__':
#     a = torch.tensor([1, 2, 3, 4, 5])
#     print(one_hot(a, depth=6))