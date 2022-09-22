import numpy as np
import json
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

class efficientnet():
    
    def __init__(self, weight_model):
        self.model = weight_model
        self.class_names = {
            0: "Spring_fall",   
            1: "Summer", 
            2: "Winter"
        }
        
    def run(self, image):
        self.image = Image.open(image)
#     def run(self):
#         self.image = Image.open("models/efficientnet/test_image/test_image_0006.jpg")
        
        tfms = transforms.Compose([transforms.Resize((300, 300)),
                           transforms.ToTensor(), 
                           transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),])
        
        self.model.eval()
        
        img = tfms(self.image).unsqueeze(0)
        
        with torch.no_grad():
            #inputs = img.to(self.device)
            inputs = img.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
            outputs = self.model(inputs)
            
            classificated_label = ""
            classificated_prob = 0
            
            for idx in torch.topk(outputs, k=3).indices.squeeze(0).tolist():
                prob = torch.softmax(outputs, dim=1)[0,idx].item()
                print('{label:<75} ({p:.2f}%)'.format(label=self.class_names[idx], p=prob*100))
                
                if classificated_label == "" or classificated_prob < prob:
                    classificated_label = self.class_names[idx]
                    classificated_prob = prob
                    
            return classificated_label
