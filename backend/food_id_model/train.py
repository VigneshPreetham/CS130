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


class Trainer():
    def __init__(self):
        self.model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b4', pretrained=True)
        self.model.classifier.fc = nn.Linear(1792, 180)

        


        self.model.to("cuda")


        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=config["lr"])
        self.batch_size = config["batch_size"]

        dataloader = DataLoader(config["data_path"], self.batch_size, False, 1)
        self.train_loader = dataloader.get_train_loader()
        self.test_loader = dataloader.get_test_loader()
        self.lr_scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, step_size=1, gamma=0.9)

        wandb.init(
            # set the wandb project where this run will be logged
            entity="mbtipredictor",
            project="recipe",
            
            # track hyperparameters and run metadata
            config= config,
        )

    

    def train(self, num_epochs):
        for epoch in range(num_epochs):
            wandb.log({"epoch": epoch})
            #log the learning rate
            wandb.log({"lr": self.optimizer.param_groups[0]['lr']})
            for (images, labels) in tqdm(self.train_loader):

                images = images.to("cuda")
                labels = labels.to("cuda")

                outputs = self.model(images)
                loss = self.criterion(outputs, labels)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                

                wandb.log({"loss": loss.item()})

            torch.save(self.model.state_dict(), f'/home/daviddu/CS130/checkpoints/eff_{epoch}.pth')
            self.test()
            self.lr_scheduler.step()
    
    def test(self):
        with torch.no_grad():
            correct = 0
            total = 0
            for (images, labels) in tqdm(self.test_loader):
                
        
                images = images.to("cuda")
                labels = labels.to("cuda")

                outputs = self.model(images)
        
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                del images, labels, outputs
            
            print(f"Accuracy: {100 * correct / total}")
            wandb.log({"accuracy": 100 * correct / total})
    
    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))

    
        

if __name__ == "__main__":
        trainer = Trainer()
        
        trainer.train(10)
        #print(trainer.model)