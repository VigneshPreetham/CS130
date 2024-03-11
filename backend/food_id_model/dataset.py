import torch
from torch.utils.data import Dataset
import pandas as pd
from PIL import Image

class FoodDataset(Dataset):
    def __init__(self, dataframe, transform=None):

        self.dataframe = dataframe
        self.transform = transform


    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()


        file_name = self.dataframe.iloc[idx, 0] 
        names = self.dataframe.iloc[idx, 2]  

        image = Image.open(file_name)
        if self.transform:
            image = self.transform(image)

        return image, names
