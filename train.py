import json
import os
from pathlib import Path
import torch.utils.data as data

import librosa
import torch
from librosa import display
import sklearn
import matplotlib.pyplot as plt
import librosa.display




import torch.nn as nn
import torch.nn.functional as F
from matplotlib import pyplot as plt
from torch import optim
from network import add_resnet_layer
from load import EcgDataset, TestDataset
from load import EcgDateLoader


device = "cuda" if torch.cuda.is_available() else 'cpu'
# loss_fn = nn.CrossEntropyLoss()
# loss_fn = loss_fn.to(device)
# n = 0
# lr = 0.02
# cur_acc = 0
# epoch = 100
# half_lr = 0
# best_val_loss = float("inf")
# pre_train_loss = float("inf")
#
# best_dir = "best_path_2"
# best_file = "best_file.pth.tar"
# Path(best_dir).mkdir(parents=True, exist_ok=True)
# best_path = os.path.join(best_dir, best_file)
#
# epoch_dir = "epoch_path_2"
# epoch_file = "epoch_file.pth.tar"
# Path(epoch_dir).mkdir(parents=True, exist_ok=True)
# epoch_path = os.path.join(epoch_dir, epoch_file)
#
# continue_dir = "continue_path_2"
# continue_file = "continue_file.pth.tar"
# Path(continue_dir).mkdir(parents=True, exist_ok=True)
# continue_path = os.path.join(continue_dir, continue_file)
#
# def train_one_epoch(data_loader):
#     model.train()
#     loss_total = 0
#     accuracy = 0
#     num = 0
#     for i, batch in enumerate(data_loader):
#         data, label = batch
#         # print(data)
#         # print(label)
#         data = data.to(device)
#         label = label.to(device)
#         out = model(data)
#         out = out.reshape((label.shape[0] * label.shape[1]), -1)
#         label = label.reshape((label.shape[0] * label.shape[1]), -1)
#         loss = loss_fn(out, label)
#         loss_total += loss
#         optimizer.zero_grad()
#         loss.backward()
#         torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
#         optimizer.step()
#         ture = label.argmax(1)
#         pred = out.argmax(1)
#         accuracy += (ture == pred).sum().item()
#         num += label.shape[0]
#     print("训练集acc{}".format(accuracy / num))
#     return loss_total
#
# def test_one_epoch(data_loader):
#     model.eval()
#     with torch.no_grad():
#         loss_total = 0
#         accuracy = 0
#         num = 0
#         for i, batch in enumerate(data_loader):
#             data, label = batch
#             # print(data)
#             # print(label)
#             data = data.to(device)
#             label = label.to(device)
#             out = model(data)
#             out = out.reshape((label.shape[0] * label.shape[1]), -1)
#             label = label.reshape((label.shape[0] * label.shape[1]), -1)
#             loss = loss_fn(out, label)
#             loss_total += loss
#             ture = label.argmax(1)
#             pred = out.argmax(1)
#             accuracy += (ture == pred).sum().item()
#             # print(label.shape)
#             num += label.shape[0]
#         print("测试集acc{}".format(accuracy / num))
#         return loss_total
# def train_one_epoch(data_loader):
#     model.train()
#     loss_total = 0
#     accuracy = 0
#     num = 0
#     for i, batch in enumerate(data_loader):
#         data, label = batch
#         data = data.to(device)
#         label = label.to(device)
#         out = model(data)
#         out = out.reshape(-1, 4)
#         label = label.reshape(-1, 4)
#         loss = loss_fn(out, label)
#         loss_total += loss
#         optimizer.zero_grad()
#         loss.backward()
#         torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
#         optimizer.step()
#         ture = label.argmax(1)
#         pred = out.argmax(1)
#         accuracy += (ture == pred).sum().item()
#         num += label.shape[0]
#         # if i % 50 == 0:
#         #     print("目前{}".format(i))
#         #     print(loss_total)
#         #     print(accuracy / num)
#     print("准确率：{}".format(accuracy / num))
#     print(loss_total)
#     return loss_total
#
# def test_one_epoch(test_loader):
#     model.eval()
#     with torch.no_grad():
#         loss_total = 0
#         accuracy = 0
#         num = 0
#         for i, batch in enumerate(test_loader):
#             data, label = batch
#             data = data.to(device)
#             label = label.to(device)
#             out = model(data)
#             out = out.reshape(-1, 4)
#             label = label.reshape(-1, 4)
#             loss = loss_fn(out, label)
#             loss_total += loss
#             pred = out.argmax(1)
#             ture = label.argmax(1)
#             accuracy += (ture == pred).sum().item()
#             num += label.shape[0]
#         print("准确率：{}".format(accuracy / num))
#         print(loss_total)
#         return loss_total
#
# if __name__ == "__main__":
#     with open("D:\code\code reappears\examples\cinc17\config.json", 'r') as f:
#         params = json.load(f)
#     model = add_resnet_layer(params)
#     model.to(device)
#     dataset = EcgDataset(params)
#     testset = TestDataset(params)
#     data_loader = EcgDateLoader(dataset, batch_size=1,
#                                 num_workers=0, shuffle=True)
#     test_loader = EcgDateLoader(testset, batch_size=1,
#                                 num_workers=0, shuffle=False)
#     # data_loader = data.DataLoader(dataset, batch_size=1,
#     #                             num_workers=0, shuffle=True)
#     # test_loader = data.DataLoader(testset, batch_size=1,
#     #                             num_workers=0, shuffle=True)
#     for j in range(n, epoch):
#         # if os.path.exists(continue_path):
#         #     continue_train = torch.load(continue_path)
#         #     model.load_state_dict(continue_train["model_state_dict"])
#         #     model.to(device)
#         #     n = continue_train["epoch"]
#         #     lr = continue_train["lr"]
#         #     pre_train_loss = continue_train["cur_loss"]
#         #     print(n)
#         #     print(lr)
#
#         if os.path.exists(best_path):
#             best_train = torch.load(best_path)
#             best_val_loss = best_train["cur_loss"]
#         optimizer = optim.Adam(model.parameters(), lr=lr)
#         # 训练模型
#         print("epoch{}".format(j))
#         train_loss = train_one_epoch(data_loader=data_loader)
#         # print("epoch:{}的训练集loss:{}".format(j, train_loss))
#         # 保存每一个epoch
#         # torch.save({"model_state_dict": model.state_dict(),
#         #             "optimizer_state_dict": optimizer.state_dict(),
#         #             "epoch": j,
#         #             "lr": lr,
#         #             "cur_loss": cur_loss_total}, epoch_dir+"\\"+"epoch_path_{}.pth.tar".format(j))
#
# #         # 测试模型
#         cur_loss_total = test_one_epoch(data_loader=test_loader)
#         # print("epoch:{}的测试集loss:{}".format(j, cur_loss_total))
#         # 保存最好的模型
#         if best_val_loss > cur_loss_total:
#             best_val_loss = cur_loss_total
#             torch.save({"model_state_dict": model.state_dict(),
#                         "optimizer_state_dict": optimizer.state_dict(),
#                         "epoch": j,
#                         "lr": lr,
#                         "cur_loss": cur_loss_total}, best_path)
#
#         if pre_train_loss > cur_loss_total:
#             best_val_loss = cur_loss_total
#             torch.save({"model_state_dict": model.state_dict(),
#                         "optimizer_state_dict": optimizer.state_dict(),
#                         "epoch": j,
#                         "lr": lr,
#                         "cur_loss": cur_loss_total}, best_path)
#             half_lr = 0
#         else:
#             half_lr += 1
#             print(half_lr)
#             if half_lr % 3 == 0:
#                 lr = lr / 2
#             if half_lr == 10:
#                 torch.save({"model_state_dict": model.state_dict(),
#                             "optimizer_state_dict": optimizer.state_dict(),
#                             "epoch": j,
#                             "lr": lr,
#                             "cur_loss": cur_loss_total}, continue_path)
#                 # break
#         # 记录断点
#         torch.save({"model_state_dict": model.state_dict(),
#                     "optimizer_state_dict": optimizer.state_dict(),
#                     "epoch": j,
#                     "lr": lr,
#                     "cur_loss": cur_loss_total}, continue_path)











import torch.nn as nn
from torch import optim
from network import add_resnet_layer
from load import EcgDataset, EcgDateLoader, TestDataset

best_dir = "best_path"
best_file = "best_file.pth.tar"
Path(best_dir).mkdir(parents=True, exist_ok=True)
best_path = os.path.join(best_dir, best_file)

epoch_dir = "epoch_path"
epoch_file = "epoch_file.pth.tar"
Path(epoch_dir).mkdir(parents=True, exist_ok=True)
epoch_path = os.path.join(epoch_dir, epoch_file)

continue_dir = "continue_path"
continue_file = "continue_file.pth.tar"
Path(continue_dir).mkdir(parents=True, exist_ok=True)
continue_path = os.path.join(continue_dir, continue_file)
#

with open("D:\code\code reappears\examples\cinc17\config.json", 'r') as f:
    params = json.load(f)
model = add_resnet_layer(params)
model.train()
model.to(device)
dataset = EcgDataset(params)
testset = TestDataset(params)
data_loader = EcgDateLoader(dataset, batch_size=1,
                            num_workers=0, shuffle=True)
test_loader = EcgDateLoader(testset, batch_size=1,
                            num_workers=0)
lr = 0.001
optimizer = optim.Adam(model.parameters(), lr=lr)
loss_fn = nn.CrossEntropyLoss()
loss_fn = loss_fn.cuda()
cur_acc = 0
epoch = 100
best_val_loss = float("inf")
pre_test_loss = float("inf")

def train_one_epoch(data_loader):
    model.train()
    loss_total = 0
    accuracy = 0
    num = 0
    for i, batch in enumerate(data_loader):
        data, label = batch
        # print(data)
        # print(label)
        data = data.to(device)
        label = label.to(device)
        out = model(data)
        out = out.reshape((label.shape[0] * label.shape[1]), -1)
        label = label.reshape((label.shape[0] * label.shape[1]), -1)
        loss = loss_fn(out, label)
        loss_total += loss
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
        optimizer.step()
        ture = label.argmax(1)
        pred = out.argmax(1)
        accuracy += (ture == pred).sum().item()
        num += label.shape[0]

    print("total_loss:{}".format(loss_total))
    print("loss:{}".format(loss_total / 239))
    print("训练集acc{}".format(accuracy / num))
    return loss_total
def test_one_epoch(data_loader):
    model.eval()
    with torch.no_grad():
        loss_total = 0
        accuracy = 0
        num = 0
        for i, batch in enumerate(data_loader):
            data, label = batch
            # print(data)
            # print(label)
            data = data.to(device)
            label = label.to(device)
            out = model(data)
            out = out.reshape((label.shape[0] * label.shape[1]), -1)
            label = label.reshape((label.shape[0] * label.shape[1]), -1)
            loss = loss_fn(out, label)
            loss_total += loss
            ture = label.argmax(1)
            pred = out.argmax(1)
            accuracy += (ture == pred).sum().item()
            # print(label.shape)
            num += label.shape[0]
        print("loss:{}".format(loss_total))
        print("loss:{}".format(loss_total / 26))
        print("测试集acc{}".format(accuracy / num))
        return loss_total
    
if __name__ == "__main__":
    half_lr = 0
    for i in range(epoch):
        print("epoch:{}".format(i))
        if half_lr == 3:
            half_lr = 0
            lr = lr * 0.001
        optimizer = optim.Adam(model.parameters(), lr=lr)
        print("------------------------------------------------------")
        train_one_epoch(data_loader=data_loader)
        print("                                                      ")
        cur_loss_total = test_one_epoch(data_loader=test_loader)
        print("------------------------------------------------------")
        if best_val_loss > cur_loss_total:
            best_val_loss = cur_loss_total
            torch.save({"model_state_dict": model.state_dict(),
                        "cur_loss": cur_loss_total,
                        "epoch": i}, best_path)
        if i % 20 == 0:
            torch.save({"model_state_dict": model.state_dict(),
                        "cur_loss": cur_loss_total,
                        "epoch": i}, epoch_path)
        if pre_test_loss > cur_loss_total:
            half_lr = 0
        else:
            half_lr += 1
