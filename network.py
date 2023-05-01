import json

import torch
import torch.nn
import torch.nn.functional as F
from torch import nn
from torchsummary import summary
import torch.utils.data as data
import argparse


device = 'cude' if torch.cuda.is_available() else 'cpu'
class _bn_relu(nn.Module):
    def __init__(self, params, dropout=0, num_features=1):
        super(_bn_relu, self).__init__()
        self.params = params
        self.dropout1 = dropout
        # print(params)
        # print(params["conv_dropout"])
        self.dt = nn.Dropout(0.2)
        self.bn = nn.BatchNorm1d(num_features=num_features, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        self.activate = nn.ReLU()
    def forward(self, x):
        x = self.bn(x)
        x = self.activate(x)
        # print(self.params["conv_dropout"])
        # print(self.dropout1)
        if self.dropout1 > 0:
            # print(111)
            # print(self.params["conv_dropout"])
            x = self.dt(x)
        return x



class add_conv_weight(nn.Module):
    def __init__(self, in_channel, num_filters, filter_length, subsample, pad_length):
        super(add_conv_weight, self).__init__()
        self.pad_length = pad_length
        self.conv = nn.Conv1d(in_channel, num_filters, filter_length, subsample)


    def forward(self, x):
        x = pad_signal(x, self.pad_length)
        x = self.conv(x)
        return x

def zeropad(x):
    y = torch.zeros_like(x)
    return torch.cat([x, y], dim=1)


def pad_signal(x, length):
    b = x.size(0)
    c = x.size(1)
    rest1 = torch.zeros(b, c, 7).type(x.type())
    rest2 = torch.zeros(b, c, 8).type(x.type())
    # rest = torch.zeros(b, c, length-1).type(x.type())
    out = torch.cat([x, rest1], 2)
    out = torch.cat([rest2, out], dim=2)
    return out


def get_num_filters_at_index(index, num_start_filters, params):
    return 2**int(index / params["conv_increase_channels_at"]) \
        * num_start_filters



class resnet_block(nn.Module):
    def __init__(self, num_filters, subsample_length, block_index, params):
        super(resnet_block, self).__init__()
        self.num_filters = num_filters
        self.subsample_length = subsample_length
        self.block_index = block_index
        self.params = params
        self.shortcut = nn.MaxPool1d(subsample_length)
        self.zero_pad = (block_index % params["conv_increase_channels_at"]) == 0 and block_index > 0
        self.conv1 = add_conv_weight(in_channel=num_filters//2, num_filters=num_filters, filter_length=params["conv_filter_length"], subsample=subsample_length, pad_length=params["conv_filter_length"])
        self.conv2 = add_conv_weight(num_filters, num_filters, params["conv_filter_length"], subsample=subsample_length, pad_length=params["conv_filter_length"])
        self.conv3 = add_conv_weight(num_filters, num_filters, params["conv_filter_length"], subsample=1, pad_length=params["conv_filter_length"])
        self.bn_relu1 = _bn_relu(dropout=0, num_features=num_filters, params=params)
        self.bn_relu2 = _bn_relu(dropout=params["conv_dropout"], num_features=num_filters, params=params)
        if (block_index % params["conv_increase_channels_at"]) == 0 \
        and block_index > 0:
            self.bn_relu1 = _bn_relu(dropout=0, num_features=num_filters // 2, params=params)
    def forward(self, x):
        # print(x.shape)
        max1 = self.shortcut(x)
        # print(max1.shape)
        if self.zero_pad is True:
            max1 = zeropad(max1)

        if self.block_index == 0:
            conv1 = self.conv2(x)
            y = self.bn_relu2(conv1)
            out = self.conv2(y)
        else:
            y = self.bn_relu1(x)
            # print(y.shape)
            if self.zero_pad is True:
                out = self.conv1(y)
            else:
                out = self.conv2(y)
            out = self.bn_relu2(out)
            out = self.conv3(out)
        return out + max1


class add_resnet_layer(nn.Module):
    def __init__(self, params):
        super(add_resnet_layer, self).__init__()
        self.conv1 = add_conv_weight(1, params["conv_num_filters_start"], params["conv_filter_length"], subsample=1, pad_length=params["conv_filter_length"])
        self.bn_relu = _bn_relu(params, dropout=0, num_features=32)
        self.res = nn.ModuleList([])
        for index, subsample_length in enumerate(params["conv_subsample_lengths"]):
            num_filters = get_num_filters_at_index(index, params["conv_num_filters_start"], params)
            self.res.append(
                resnet_block(num_filters, subsample_length, index, params)
            )
        # print(params)
        self.bn_relu2 = _bn_relu(params, dropout=0, num_features=256)
        self.dense = nn.Linear(256, 4)
        self.activate = nn.Softmax(dim=2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn_relu(x)
        # print(x.shape)
        for i in range(len(self.res)):
            x = self.res[i](x)
            # print(x.shape)
        x = self.bn_relu2(x)
        x = x.transpose(1, 2)
        x = self.dense(x)
        # print(x.shape)
        x = self.activate(x)
        return x
def train_network(params):
    net = add_resnet_layer(params)
    net(params["input_shape"])
asd = {
    "conv_subsample_lengths": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    "conv_filter_length": 16,
    "conv_num_filters_start": 32,
    "conv_init": "he_normal",
    "conv_activation": "relu",
    "conv_dropout": 0.2,
    "conv_num_skip": 2,
    "conv_increase_channels_at": 4,
    "learning_rate": 0.001,
    "batch_size": 32,
    "generator": True,
    "save_dir": "saved"
}




#
#
# # net = add_resnet_layer(**asd)
# # summary(net, input_size=(1, 256))
# # print(net)
# # parser = argparse.ArgumentParser()
# # parser.add_argument("config_file", help="path to config file")
# #
# args = parser.parse_args()
params = json.load(open("D:\\code\\ecg_pytorch\\examples\\cinc17\\config.json", 'r'))
#
# print(params)
# a = torch.rand([2, 1, 256], dtype=torch.float32)
# print(a.shape)
# net_conv = add_conv_weight(1, 32, 16, 1)
# out1 = net_conv(a)
# print(out1.shape)

net = add_resnet_layer(params)
# a = torch.rand([32, 1, 512])
# out = net(a)
# print()
# net.to(device)
net.eval()
summary(net, input_size=(1, 256))
# # print(net)
# # out = net(a)
# # print(out.shape)
# # print()
# # print(net)
#
#
#
#
#
#
#
# #
# # a = torch.randn((1, 1, 2))
# # # print(a.shape)
# # net = ecg_net()
# # out = net(a)
# #
# # print(out.shape)


#
#
# import json
#
# import torch
# import torch.nn
# import torch.nn.functional as F
# from torch import nn
# import torch.utils.data as data
# import argparse
#
#
#
# class _bn_relu(nn.Module):
#     def __init__(self, params, dropout=0, num_features=1):
#         super(_bn_relu, self).__init__()
#         self.params = params
#         self.dropout1 = dropout
#         # print(params)
#         # print(params["conv_dropout"])
#         self.dt = nn.Dropout(0.2)
#         self.bn_relu = nn.BatchNorm1d(num_features=num_features)
#
#     def forward(self, x):
#         x = F.relu(self.bn_relu(x))
#         # print(self.params["conv_dropout"])
#         # print(self.dropout1)
#         if self.dropout1 > 0:
#             # print(111)
#             # print(self.params["conv_dropout"])
#             x = F.dropout(x)
#         return x
#
#
#
# class add_conv_weight(nn.Module):
#     def __init__(self, in_channel, num_filters, filter_length, subsample, pad_length):
#         super(add_conv_weight, self).__init__()
#         self.pad_length = pad_length
#         self.conv = nn.Conv1d(in_channel, num_filters, filter_length, subsample)
#
#     def forward(self, x):
#         x = pad_signal(x, self.pad_length)
#         x = self.conv(x)
#         return x
#
# def zeropad(x):
#     y = torch.zeros_like(x)
#     return torch.cat([x, y], dim=1)
#
#
# def pad_signal(x, length):
#     b = x.size(0)
#     c = x.size(1)
#     rest = torch.zeros(b, c, length-1).type(x.type())
#     out = torch.cat([x, rest], 2)
#     return out
#
#
# def get_num_filters_at_index(index, num_start_filters, params):
#     return 2**int(index / params["conv_increase_channels_at"]) \
#         * num_start_filters
#
#
# class resnet_block(nn.Module):
#     def __init__(self, num_filters, subsample_length, block_index, params):
#         super(resnet_block, self).__init__()
#         self.num_filters = num_filters
#         self.subsample_length = subsample_length
#         self.block_index = block_index
#         self.params = params
#         # print(num_filters)
#         # print(subsample_length)
#         # print(block_index)
#         # print(params)
#
#         self.shortcut = nn.MaxPool1d(subsample_length)
#         self.zero_pad = (block_index % params["conv_increase_channels_at"]) == 0 and block_index > 0
#
#         self.conv1 = add_conv_weight(in_channel=num_filters//2, num_filters=num_filters, filter_length=params["conv_filter_length"], subsample=subsample_length, pad_length=params["conv_filter_length"])
#         self.conv2 = add_conv_weight(num_filters, num_filters, params["conv_filter_length"], subsample=subsample_length, pad_length=params["conv_filter_length"])
#         self.conv3 = add_conv_weight(num_filters, num_filters, params["conv_filter_length"], subsample=1, pad_length=params["conv_filter_length"])
#
#         self.bn_relu1 = _bn_relu(dropout=0, num_features=num_filters, params=params)
#         self.bn_relu2 = _bn_relu(dropout=params["conv_dropout"], num_features=num_filters, params=params)
#
#         if (block_index % params["conv_increase_channels_at"]) == 0 \
#         and block_index > 0:
#             self.bn_relu1 = _bn_relu(dropout=0, num_features=num_filters // 2, params=params)
#
#
#     def forward(self, x):
#         # print(x.shape)
#         max1 = self.shortcut(x)
#         # print(max1.shape)
#         if self.zero_pad is True:
#             max1 = zeropad(max1)
#
#         if self.block_index == 0:
#             conv1 = self.conv2(x)
#             y = self.bn_relu2(conv1)
#             out = self.conv2(y)
#             # print(out.shape)
#         else:
#             y = self.bn_relu1(x)
#             # print(y.shape)
#             if self.zero_pad is True:
#                 out = self.conv1(y)
#             else:
#                 out = self.conv2(y)
#             out = self.bn_relu2(out)
#             out = self.conv3(out)
#
#
#         # print(out.shape)
#         # print(max1.shape)
#         return out + max1
#
#
# class add_resnet_layer(nn.Module):
#     def __init__(self, params):
#         super(add_resnet_layer, self).__init__()
#         self.conv1 = add_conv_weight(1, params["conv_num_filters_start"], params["conv_filter_length"], subsample=1, pad_length=params["conv_filter_length"])
#         # print(1)
#         self.bn_relu = _bn_relu(params, dropout=params["conv_dropout"], num_features=32)
#
#         self.res = nn.ModuleList([])
#         for index, subsample_length in enumerate(params["conv_subsample_lengths"]):
#             num_filters = get_num_filters_at_index(index, params["conv_num_filters_start"], params)
#             # print(num_filters)
#             self.res.append(
#                 resnet_block(num_filters, subsample_length, index, params)
#             )
#         # print(params)
#         self.bn_relu2 = _bn_relu(params, dropout=0, num_features=256)
#         self.dense = nn.Linear(256, 4)
#
#     def forward(self, x):
#         # print(x.shape)
#         x = self.conv1(x)
#         x = self.bn_relu(x)
#         # print(x.shape)
#         for i in range(len(self.res)):
#             # print(i)
#             # print(x.shape)
#             x = self.res[i](x)
#         # print(x.shape)
#         # x = x.squeeze()
#         # print(x.shape)
#         x = self.bn_relu2(x)
#         x = x.transpose(1, 2)
#         x = self.dense(x)
#
#         return x
#
#
# def train_network(params):
#     net = add_resnet_layer(params)
#     net(params["input_shape"])
#
#
# if __name__ == '__main__':
#     p = {
#         "conv_subsample_lengths": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
#         "conv_filter_length": 16,
#         "conv_num_filters_start": 32,
#         "conv_init": "he_normal",
#         "conv_activation": "relu",
#         "conv_dropout": 0.2,
#         "conv_num_skip": 2,
#         "conv_increase_channels_at": 4,
#
#         "learning_rate": 0.001,
#         "batch_size": 32,
#
#         "input_shape": [1, 256],
#
#         "train": "D:\\code\\code reappears\\examples\\cinc17\\train.json",
#         "dev": "D:\\code\\code reappears\\examples\\cinc17\\dev.json",
#
#         "generator": True,
#
#         "save_dir": "saved"
#     }
#     # a = torch.rand([32, 1, 2816])
#     # print(a.shape)
#     net = add_resnet_layer(p)
#     # b = net(a)
#     # print(b.shape)
#     # k = sum(p.numel() for p in net.parameters() if p.requires_grad)
#     # print('# of parameters:', k)
#     from torchsummary import summary
#     summary(net, input_size=(1, 256))

# net = add_resnet_layer(**asd)
# print(net)
# parser = argparse.ArgumentParser()
# parser.add_argument("config_file", help="path to config file")
#
# args = parser.parse_args()
# params = json.load(open("D:\\data\\code reappears\\examples\\cinc17\\config.json", 'r'))

# print(params)
# a = torch.rand([2, 1, 256], dtype=torch.float32)
# print(a.shape)
# net_conv = add_conv_weight(1, 32, 16, 1)
# out1 = net_conv(a)
# print(out1.shape)
# net = add_resnet_layer(params)
# print(net)
# out = net(a)
# print(out.shape)
# print()
# print(net)







#
# a = torch.randn((1, 1, 2))
# # print(a.shape)
# net = ecg_net()
# out = net(a)
#
# print(out.shape)
