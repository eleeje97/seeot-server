import torch
from .efficientnet_pytorch import EfficientNet

class Load_Model():

    def __init__(self):
        # load model's weight
        self.checkpoint_m = 'models/efficientnet/checkpoint/male_classification_model.pt'
        self.checkpoint_f = 'models/efficientnet/checkpoint/female_classification_model.pt'
        
        self.model_name = 'efficientnet-b3'  # b3
        self.model = EfficientNet.from_pretrained(self.model_name, num_classes=3)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # set gpu
        
        self.model_m = self.model.to(self.device)
        self.model_f = self.model.to(self.device)
        
        self.model_m.load_state_dict(torch.load(self.checkpoint_m))
        self.model_f.load_state_dict(torch.load(self.checkpoint_f))

        
        
    def set_model(self):
        return self.model_m, self.model_f
