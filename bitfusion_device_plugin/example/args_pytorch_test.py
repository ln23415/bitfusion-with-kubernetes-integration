import argparse
import torch
import torchvision
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
import torch.optim as optim
import time

import numpy as np


parser = argparse.ArgumentParser(description="test")

parser.add_argument('-n', '--batchsize', type=int, help="this is batchsize")
parser.add_argument('-p', '--pvar', help="this is pvar")
args = parser.parse_args()

print("########################")
print("-n arg: " + str(args.batchsize))
print("-p arg: " + str(args.pvar))
print("########################")


batch_size = args.batchsize
learning_rate = 1e-3

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]  
)

trainset = torchvision.datasets.CIFAR10(root="/benchmark/data/train", train=True, download=True, transform=transform) 

trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True) 

testset = torchvision.datasets.CIFAR10(root="/benchmark/data/test", train=False, download=True, transform=transform) 

testloader = torch.utils.data.DataLoader(testset, batch_size=10000, shuffle=True) 

test_data_iter = iter(testloader) 
test_img, test_label = test_data_iter.next()  

test_img = test_img.to(device)
test_label = test_label.to(device)

classes = ("plane", "car", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck")



print("use resnet18 as backbone...")

Mynet = models.resnet18(pretrained=False)
fc_inputs = Mynet.fc.in_features
Mynet.fc = nn.Sequential(
    nn.Linear(fc_inputs, 256),
    nn.ReLU(),
    nn.Linear(256, 10),
    nn.LogSoftmax(dim=1)
)


loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(Mynet.parameters(), lr=learning_rate)

print("begin to train...")

Mynet = Mynet.to(device)
for epoch in range(1): 
    start_t = time.time()
    running_loss = 0.
    for step, data in enumerate(trainloader, start=0): 
        inputs, labels = data
        inputs = inputs.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()

        outputs = Mynet(inputs)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if step % 100 == 99: 
            with torch.no_grad():  
                outputs = Mynet(test_img)  
                y_pred = torch.max(outputs, dim=1)[1]  
                accuracy = (y_pred == test_label).sum().item() / test_label.size(0) 

                print('[%d, %5d] train_loss: %.3f  test_accuracy: %.3f' %
                          (epoch + 1, step + 1, running_loss / 500, accuracy)) 
                running_loss = 0.0
    end_t = time.time()
    print("time cost of this epoch is ", str(end_t-start_t))
print("Training finished")

