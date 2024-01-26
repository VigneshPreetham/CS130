import torch
import torch.nn.functional as F
from torch import nn, Tensor





class Inception3(nn.Module):
    def __init__(self, num_classes = 1000, dropout = 0.5):
        super().__init__()

        conv_block = Conv2D
        inception_a = InceptionA
        inception_b = InceptionB
        ## Need to do inception C, D, E and AUX

       
        self.conv1 = conv_block(3, 32, kernel_size=3, stride=2)
        self.conv2 = conv_block(32, 32, kernel_size=3)
        self.conv3 = conv_block(32, 64, kernel_size=3, padding=1)
        self.maxpool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.conv4 = conv_block(64, 80, kernel_size=1)
        self.conv5 = conv_block(80, 192, kernel_size=3)
        self.maxpool2 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.inception_a1 = inception_a(192, dim=32)
        self.inception_a2 = inception_a(256, dim=64)
        self.inception_a3 = inception_a(288, dim=64)
        self.inception_b1 = inception_b(288)



        self.dropout = nn.Dropout(p=dropout)
        self.fc = nn.Linear(2048, num_classes)
      

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.maxpool1(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.maxpool2(x)
        x = self.inception_a1(x)
        x = self.inception_a2(x)
        x = self.inception_a3(x)
        x = self.inception_b1(x)

        #Inception C, D, E 
        #AUX need to do
  
    
        x = self.dropout(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
 


class InceptionA(nn.Module):
    def __init__(self, in_channels, dim, conv_block = None):
        super().__init__()
 
        conv_block = Conv2D

        self.branch1x1 = conv_block(in_channels, 64, kernel_size=1)

        self.branch5x5_1 = conv_block(in_channels, 48, kernel_size=1)
        self.branch5x5_2 = conv_block(48, 64, kernel_size=5, padding=2)

        self.branch3x3_1 = conv_block(in_channels, 64, kernel_size=1)
        self.branch3x3_2 = conv_block(64, 96, kernel_size=3, padding=1)
        self.branch3x3_3 = conv_block(96, 96, kernel_size=3, padding=1)

        self.pool = conv_block(in_channels, dim, kernel_size=1)

    def forward(self, x):
        a = self.branch1x1(x)

        b = self.branch5x5_1(x)
        b = self.branch5x5_2(b)

        c = self.branch3x3_1(x)
        c = self.branch3x3_2(c)
        c = self.branch3x3_3(c)

        pool = F.avg_pool2d(x, kernel_size=3, stride=1, padding=1)
        pool = self.pool(pool)

        outputs = [a, b, c, pool]
        return torch.cat(outputs, 1)



class InceptionB(nn.Module):
    def __init__(self, in_channels, conv_block = None):
        super().__init__()
  
        conv_block = Conv2D

        self.branch3x3 = conv_block(in_channels, 384, kernel_size=3, stride=2)

        self.branch3x3_1 = conv_block(in_channels, 64, kernel_size=1)
        self.branch3x3_2 = conv_block(64, 96, kernel_size=3, padding=1)
        self.branch3x3_3 = conv_block(96, 96, kernel_size=3, stride=2)

    def forward(self, x):
        a = self.branch3x3(x)

        b = self.branch3x3_1(x)
        b = self.branch3x3_2(b)
        b = self.branch3x3_3(b)

        pool = F.max_pool2d(x, kernel_size=3, stride=2)

        outputs = [a, b, pool]

        return torch.cat(outputs, 1)


class Conv2D(nn.Module):
    def __init__(self, in_channels, out_channels) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False)
        self.bn = nn.BatchNorm2d(out_channels, eps=0.001)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        return F.relu(x, inplace=True)

