import numpy as np
import torch
import torch.nn as nn
from torchvision import datasets
from torchvision import transforms, models
from torch.utils.data.sampler import SubsetRandomSampler
from tqdm import tqdm


class DataLoader():
    def __init__(self, data_dir, batch_size, augment, random_seed, valid_size=0.1, shuffle=True):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.augment = augment
        self.random_seed = random_seed
        self.valid_size = valid_size
        self.shuffle = shuffle
        
    def get_train_valid_loader(self):
        normalize = transforms.Normalize(
            mean=[0.4913997551666284, 0.48215855929893703, 0.4465309133731618],
        std=[0.24703225141799082, 0.24348516474564, 0.26158783926049628],
        )


        valid_transform = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        if self.augment:
            train_transform = transforms.Compose([
                transforms.Resize(299),
                transforms.CenterCrop(299),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
        else:
            train_transform = transforms.Compose([
                transforms.Resize(299),
                transforms.CenterCrop(299),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])


        train_dataset = datasets.CIFAR10(
            root=self.data_dir, train=True,
            download=True, transform=train_transform,
        )

        valid_dataset = datasets.CIFAR10(
            root=self.data_dir, train=True,
            download=True, transform=valid_transform,
        )

        num_train = len(train_dataset)
        indices = list(range(num_train))
        split = int(np.floor(self.valid_size * num_train))

        if self.shuffle:
            np.random.seed(self.random_seed)
            np.random.shuffle(indices)

        train_idx, valid_idx = indices[split:], indices[:split]
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)

        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=self.batch_size, sampler=train_sampler, drop_last=True)
    
        valid_loader = torch.utils.data.DataLoader(
            valid_dataset, batch_size=self.batch_size, sampler=valid_sampler, drop_last=True)


        return (train_loader, valid_loader)


    def get_test_loader(self):
        normalize = transforms.Normalize(
            mean=[0.4913997551666284, 0.48215855929893703, 0.4465309133731618],
        std=[0.24703225141799082, 0.24348516474564, 0.26158783926049628],
        )


        transform = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        dataset = datasets.CIFAR10(
            root=self.data_dir, train=False,
            download=True, transform=transform,
        )

        data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=self.batch_size, shuffle=self.shuffle, drop_last=True
        )

        return data_loader