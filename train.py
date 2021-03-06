
import torch
import torch.nn as nn
from torchvision.utils import make_grid
from torchvision.utils import save_image
from IPython.display import Image
import matplotlib.pyplot as plt
import numpy as np
import random

import os
from torchvision import transforms

import PIL
from pathlib import Path
from PIL import Image
from torchvision.models import vgg19_bn
import glob
from torch.autograd import Variable
import model as md
import dataloader
# from torch.utils.tensorboard import SummaryWriter
random.seed(0)

log_dir = "~/logs"
# writer = SummaryWriter(log_dir)
device = "cuda:0" if torch.cuda.is_available() else "cpu"
def main(epoch_num=10,learning_rate = 0.01):
    
    root = Path(os.getcwd())
    print(root)
    image_dir = root/'covid_safavi/sample/4173146/lung_white'
    csv_file = root/'dataset/label.csv'
    transform_img = transforms.Compose([
        transforms.ToTensor()
])
    dset = dataloader.covid_ct(root, image_dir, csv_file, transform=transform_img)
    train_loader =  dataloader.DataLoader(dset, batch_size=2, drop_last=False, shuffle=True)
    #visualize
    # plt.figure(figsize=(20,10))
    # plt.imshow(dset[0][0][3].numpy().astype('uint16'))
    #hyper parameter

   
    Model = md.Net()
    Model.to(device ='cuda:0')
    criterion = nn.CrossEntropyLoss()

    learning_rate = 0.01
    optimizer = torch.optim.SGD(Model.parameters(), lr = learning_rate, momentum=0.9)
    num_epoch = epoch_num
    running_loss = 0.0    
    for epoch in range(num_epoch):
        print("----------------------------",epoch,"///",num_epoch)
        correct = 0
        total = 0
        optimizer.zero_grad()
        for i, data in enumerate(train_loader, 0):
            # zero the parameter gradients
            with torch.enable_grad():
                inputs, labels = data

                images = inputs.to(device).requires_grad_() 
                labels = labels.to(device)
               
                inputs = Variable(images).type(torch.FloatTensor)
                targets = Variable(labels).type(torch.LongTensor)
                targets = targets.unsqueeze(0)
                outputs = Model(inputs.cuda())
                print("-----",targets,outputs)
                loss = criterion(outputs,torch.max(targets.cuda(),1)[1]).type(torch.FloatTensor)
                loss.backward()
                print("update weight")
                optimizer.zero_grad()
                total += labels.size(0)
                correct += (outputs == targets.cuda()).sum().item()
                running_loss += loss.item()
            if i % 100 == 0:    # print every 100 mini-batches
                print('[%d, %5d] loss: %.3f' %
                    (epoch + 1, i + 1, running_loss / 100))
                print('Accuracy of the network : %d %%' % (
        100 * correct / total))
                running_loss = 0.0
                

        

    print('Finished Training')




if __name__ == "__main__":
    main()