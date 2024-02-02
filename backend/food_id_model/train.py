import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from inception import InceptionV3
from config import config


class Trainer():
    def __init__(self):
        self.model = model

        self.model = model = InceptionV3()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(model.parameters(), lr=config["lr"])
        self.batch_size = config["batch_size"]

        dataloader = DataLoader(config["data_path"], self.batch_size, False, 1)
        self.train_loader, self.valid_loader = dataloader.get_train_valid_loader()
        self.test_loader = dataloader.get_test_loader()
    

    def train(self, num_epochs):
        for epoch in range(num_epochs):
            for i, (images, labels) in enumerate(self.train_loader):

                outputs = self.model(images)
                loss = self.criterion(outputs, labels)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                #wandb logging soon

            torch.save(self.model.state_dict(), f'./ML/food_id_model/checkpoints/inception_{epoch}.pth')





