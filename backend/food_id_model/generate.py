import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


from config import config
from dataloader import DataLoader
from tqdm import tqdm
import wandb
import pickle as pkl
from PIL import Image


class Generator():
    def __init__(self, path=None):
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'inception_v3', pretrained=True)
        num_features = self.model.fc.in_features 
        self.model.fc = torch.nn.Linear(num_features, 498)
        self.transform = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
        ])
        self.path = path

        self.labels_to_food = pkl.load(open("label_to_food.pkl", "rb"))

        if path:
            self.load_model()
    

    # image is a PIL image generate should return the name of the food
    def generate(self, image):
        with torch.no_grad():
            self.model.eval()
            image = self.transform(image).unsqueeze(0)

            output = self.model(image)
            predicted = torch.argmax(output, 1)
            return self.labels_to_food[predicted.item()]

        

    def load_model(self):
        self.model.load_state_dict(torch.load(self.path))

    
        

if __name__ == "__main__":
    generator = Generator()
    path = ""
    image = Image.open(path)
    print(generator.generate(image))
    
