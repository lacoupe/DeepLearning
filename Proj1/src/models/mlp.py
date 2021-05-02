import torch
import torch.nn as nn
from models.custom import SizeableModule, NamedModule, WeightInitializableModule


class MLP(SizeableModule, NamedModule, WeightInitializableModule):
    """Multi Layer Perceptron 

    Attributes:
        fc1 ([type]): Fully connected linear layer (2*14*14) -> 128
        fc2 ([type]): [description]
        fc3 ([type]): [description]
        fc4 ([type]): [description]
    """
    
    def __init__(self):

        super(MLP, self).__init__()
        self.fc1 = nn.Linear(2 * 14 * 14, 128)
        self.fc2 = nn.Linear(128, 98)
        self.fc3 = nn.Linear(98, 49)
        self.fc4 = nn.Linear(49, 10)
        
        self.classifier = nn.Linear(10, 1)
        
        # dropout layer
        self.drop = nn.Dropout(0.2)
        
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
        # Initialize weights
        self.apply(self.weights_init)
        
    def forward(self, x: torch.tensor) -> torch.tensor:
        """
        Forward pass function for the global siamese CNN

        Args:
            x [float32]: input images with dimension Bx2x14x14 (for batch size B)

        Returns:
            [int]: predicted probability ]0,1[
            [float32] : predicted classe by pair, size Bx2x10
        """
        # flatten image input
        x = x.flatten(start_dim=1)  # (-1, 2 x 14 x 14)
        # add hidden layer, with relu activation function
        x = self.relu(self.fc1(x))
        x = self.drop(x)
        
        x = self.relu(self.fc2(x))
        x = self.drop(x)
        
        x = self.relu(self.fc3(x))
        x = self.drop(x)
        
        x = self.fc4(x)
        x = self.sigmoid(self.classifier(x))
        
        return x.squeeze(), None
    
    def __str__(self) -> str:
        """Representation"""
        return "Multi-Layer Perceptron"
