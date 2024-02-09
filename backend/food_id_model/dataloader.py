import numpy as np
import torch
import torch.nn as nn
from torchvision import datasets
from torchvision import transforms, models
from torch.utils.data.sampler import SubsetRandomSampler
from tqdm import tqdm
from dataset import FoodDataset
import pandas as pd

class DataLoader():
    def __init__(self, data_dir, batch_size, augment, random_seed, valid_size=0.1, shuffle=True):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.augment = augment
        self.random_seed = random_seed
        self.valid_size = valid_size
        self.shuffle = shuffle

        
    def get_train_loader(self):


        train_transform = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
        ])


        train_df = pd.read_csv(self.data_dir + '/train.csv')
        train_dataset = FoodDataset(train_df, transform=train_transform)

        
        num_train = len(train_dataset)
        indices = list(range(num_train))
 

        if self.shuffle:
            np.random.seed(self.random_seed)
            np.random.shuffle(indices)


  

        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=self.batch_size, shuffle=self.shuffle, drop_last=True)
    



        return train_loader


    def get_test_loader(self):


        valid_transform = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
        ])

        valid_df = pd.read_csv(self.data_dir + '/val.csv')
        valid_dataset = FoodDataset(valid_df, transform=valid_transform)


        data_loader = torch.utils.data.DataLoader(
            valid_dataset, batch_size=self.batch_size, shuffle=self.shuffle, drop_last=True
        )

        return data_loader