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
        self.model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b4', pretrained=False)
        self.model.classifier.fc = nn.Linear(1792, 180)
        self.transform =  transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(256),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),

        ])
        self.path = path

        self.labels_to_food = pkl.load(open("idx_to_food.pkl", "rb"))

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
    path = "/home/daviddu/CS130/backend/food_id_model/datasets/food-classification/train/Apple pie/134.jpg"
    image = Image.open(path)
    print(generator.generate(image))
    
