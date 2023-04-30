from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import json
from util import one_hot
# import keras
import numpy as np
import os
import random
import scipy.io as sio
import tqdm
import torch
import torch.utils.data as data
from network import add_resnet_layer


STEP = 256
def data_generator(batch_size, preproc, x, y):
    num_examples = len(x)
    # print(len(x))
# 就是对应位置的组成元组
    examples = zip(x, y)
    # x[0]对应的是有、列表的长度
    examples = sorted(examples, key=lambda x: x[0].shape[0])
    # for i in range(len(examples)):
        # print(examples[i][0].shape)
        # print(len(examples[i][1]))
    # print(examples[0])
    # print(len(x[1]))
    # print(type(x))
    # for i in range(len(x)):
    #     print(x[i])
    #     print(x[i].shape[0])
    # print(len(examples))
    # for i in range(len(examples)):
    #     print(len(examples[i][0]))
    # print(len(x[0]))
    end = num_examples - batch_size + 1
    batches = [examples[i:i+batch_size]
                for i in range(0, end, batch_size)]
    # print(type(batches))
    # print(len(batches))
    # return batches
    # random.shuffle(batches)
    # print(len(batches))
    # count = 0
    mini_batch = []
    while True:
        for batch in batches:
        # print(count)
            # print(batch)
            x, y = zip(*batch)
            x = preproc.process_x(x)
            y = preproc.process_y(y)
            # print(type(x))
            # print(x)
            # print(type(y))
            mini_batch.append([x, y])

        return mini_batch
        # print(mini_batch[0])


class Preproc:
    def __init__(self, ecg, labels):
        self.mean, self.std = compute_mean_std(ecg)
        self.classes = list(sorted(set(l for label in labels for l in label)))
        # print(len(labels))
        # print(l for label in labels for l in label)
        # print(self.classes)
        # self.int_to_class = dict(zip(range(len(self.classes)), self.classes))
        # print(self.int_to_class)
        # self.class_to_int = {c : i for i, c in self.int_to_class.items()}
        # print(self.class_to_int)
        self.int_to_class = {key: ii for key, ii in enumerate(self.classes)}
        self.class_to_int = {key: ii for ii, key in enumerate(self.classes)}
        # print(self.int_to_class)
        # print(self.class_to_int)

    def process(self, x, y):
        return self.process_x(x), self.process_y(y)

    def process_x(self, x):
        x = pad(x)
        x = (x - self.mean) / self.std
        # print(x.shape)
        # x = x[:,:]
        # print(x.shape)
        # print(type(x))
        return x

    def process_y(self, y):
        # TODO, awni, fix hack pad with noise for cinc
        # print(len(y))
        y = pad([[self.class_to_int[c] for c in s] for s in y], val=3, dtype=np.int32)
        # print(len(y))

        # for i in range(len(y)):
        #     print(y[i])
        # print(len(self.classes))
        # print(y)
        # y =
        # print(type(y))
        list_ont_hot = []
        for i in range(len(y)):
            list_ont_hot.append(one_hot(y[i], depth=len(self.classes)))
        # torch.cat(list_ont_hot, dim=0).reshape(len(y), -1, self.classes)
        # y = keras.utils.np_utils.to_categorical(
        #         y, num_classes=len(self.classes))
        list_ont_hot = torch.cat(list_ont_hot, dim=0).reshape(len(y), -1, len(self.classes))
        # list_ont_hot = torch.cat(list_ont_hot, dim=0)
        # print(list_ont_hot.shape)
        return list_ont_hot

def pad(x, val=0, dtype=np.float32):
    max_len = max(len(i) for i in x)
    padded = np.full((len(x), max_len), val, dtype=dtype)
    for e, i in enumerate(x):
        padded[e, :len(i)] = i
    return padded

def compute_mean_std(x):
    x = np.hstack(x)
    return (np.mean(x).astype(np.float32),
           np.std(x).astype(np.float32))

def load_dataset(data_json):
    with open(data_json, 'r') as fid:
        data = [json.loads(l) for l in fid]
    labels = []; ecgs = []
    for d in tqdm.tqdm(data):
        labels.append(d['labels'])
        # print(d['ecg'])
        ecgs.append(load_ecg(d['ecg']))
    return ecgs, labels

def load_ecg(record):
    if os.path.splitext(record)[1] == ".npy":
        print(1)
        ecg = np.load(record)
    elif os.path.splitext(record)[1] == ".mat":
        # print(2)
        ecg = sio.loadmat(record)['val'].squeeze()
        # print(type(ecg))
    else: # Assumes binary 16 bit integers
        print(3)
        with open(record, 'r') as fid:
            ecg = np.fromfile(fid, dtype=np.int16)

    trunc_samp = STEP * int(len(ecg) / STEP)
    # print(trunc_samp)
    return ecg[:trunc_samp]

class TestDataset(data.Dataset):
    def __init__(self, params):
        super(TestDataset, self).__init__()
        dev = load_dataset(params["dev"])
        preproc = Preproc(*dev)
        # print("Training size: " + str(len(dev[0])) + " examples.")
        # print("Dev size: " + str(len(dev[0])) + " examples.")

        params.update({
            "num_catagories": len(preproc.classes)
        })
        print(params)
        batch_size = params.get("batch_size", 32)
        self.minibatch = data_generator(batch_size, preproc, *dev)
        # print(self.minibatch)

    def __getitem__(self, index):
        return self.minibatch[index]

    def __len__(self):
        return len(self.minibatch)




class EcgDataset(data.Dataset):
    def __init__(self, params):
        super(EcgDataset, self).__init__()
        train = load_dataset(params["train"])
        preproc = Preproc(*train)
        # print("Training size: " + str(len(train[0])) + " examples.")

        params.update({
            "num_catagories": len(preproc.classes)
        })
        # print(params)
        batch_size = params.get("batch_size", 32)
        self.minibatch = data_generator(batch_size, preproc, *train)
        # print(self.minibatch)

    def __getitem__(self, index):
        return self.minibatch[index]

    def __len__(self):
        return len(self.minibatch)


class EcgDateLoader(data.DataLoader):
    def __init__(self, *args, **kwargs):
        super(EcgDateLoader, self).__init__(*args, **kwargs)
        self.collate_fn = _collate_fn
        # print(11111111111)
def _collate_fn(batch):
    assert len(batch) == 1

    data1, label1 = batch[0]
    data1 = torch.tensor(data1)
    data1 = torch.unsqueeze(data1, dim=1)
    return data1, label1

if __name__ == '__main__':
    mat_path = 'D:/code/ecg_pytorch/examples/cinc17/data/training2017/A04352.mat'
    data = sio.loadmat(mat_path)
    print(data)

# def _collate_fn(batch):
#     assert len(batch) == 1
#     # print(batch[0])
#     # print(batch)
#     data1, label = loader_data_and_label(batch[0])
#
#     data1 = torch.tensor(data1)
#     data1 = torch.unsqueeze(data1, dim=1)
#     # print(data1)
#     # print(data1.shape)
#     # print(label.shape)
#     return data1, label
#
#
# def loader_data_and_label(batch):
#     segment = 256
#     data2, label = [], []
#     row_data, label = batch
#     # print(row_data)
#     # print(type(label))
#     utt_len = row_data.shape[-1]
#     for i in range(row_data.shape[0]):
#         for j in range(0, utt_len - segment + 1, segment):
#             data2.append(row_data[i][j:j+segment])
#     return data2, label



# if __name__ == '__main__':
#     with open("D:\code\code reappears\examples\cinc17\config.json", 'r') as f:
#         params = json.load(f)
#     dataset = EcgDataset(params)
#     dataload = EcgDateLoader(dataset, batch_size=1, num_workers=0)
#     # dataload = data.DataLoader(dataset, batch_size=1, num_workers=0)
#     net = add_resnet_layer(params)
#     for i, batch in enumerate(dataload):
#         data, label = batch
#         print(data.shape)
#         print(label.shape)
#         print(label)
#         # data = torch.squeeze(data)
#         # data = torch.unsqueeze(data, dim=1)
#         # label = torch.squeeze(label)
#         # out = net(data)
#         # print(out.shape)
#         # print(label.shape)
#         # label = torch.squeeze(label)
#         # print(data.shape)
#         # print(label.shape)
#         break
    # params = json.load(open("D:\\code\\code reappears\\examples\\cinc17\\train.json", 'r'))
    # dataset = EcgDataset("D:\\code\\code reappears\\examples\\cinc17\\train.json")

#
# if __name__ == "__main__":
#     data_json = "D:\\code\\code reappears\\examples\\cinc17\\train.json"
#     train = load_dataset(data_json)
#     preproc = Preproc(*train)
#     gen = data_generator(32, preproc, *train)
#     count = 0
#     for x, y in gen:
#         count += 1
#         print(x.shape, y.shape)
#         print(x)
#         print(y)
#         # print(y)
#         break
#
#     print(count)
