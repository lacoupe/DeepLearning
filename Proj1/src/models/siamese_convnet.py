import torch
from torch import nn

from models.custom import SizeableModule, NamedModule


class SiameseConvNet(SizeableModule, NamedModule):
    """
    Siamese Convolutional Network Module

    Attributes:
        conv1 (nn.Conv2d)     : fist convolutional layer
        conv2 (nn.Conv2d)     : second convolutional layer
        fc1 (nn.Linear)       : first fully connected layer
        fc2 (nn.Linear)       : second fully connected layer
        fc3 (nn.Linear)       : third fully connected layer
        fc4 (nn.Linear)       : last fully connected layer
        drop (nn.Dropout)     : dropout function
        drop2d (nn.Dropout)   : dropout function that drop entires channels
        pool (nn.MaxPool2d)   : maxpool function
        relu (nn.Relu)        : relu activation function
        sigmoid (nn.Sigmoid)  : sigmoid activation function
    """
    
    def __init__(self):
        """Initialize Siamese Convolutional Neural Network"""
        super().__init__()
    
        # convolutional layers
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)   # 32x(14-2)x(14-2) = 16x12x12
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)  # 64x10x10  => pooling = 64x5x5
        
        # fully connected layers
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10)
        self.fc3 = nn.Linear(20, 10)
        self.fc4 = nn.Linear(10, 1)
        
        # regularizers
        self.drop = nn.Dropout(0.1)
        self.drop2d = nn.Dropout2d(0.1)
        self.pool = nn.MaxPool2d(kernel_size=2)
        self.bn2d = nn.BatchNorm2d(32)
        self.bn = nn.BatchNorm1d(128)

        # activation functions
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward_once(self, x):
        """
        Forward pass function used in the sub-network

        Args:
            x [float32]: input image with dimension Bx1x14x14 (for batch size B)

        Returns:
            [float32]: non activated tensor of dimension Bx1x10
        """

        x = self.drop(self.conv1(x))
        x = self.relu(x)

        x = self.drop2d(self.conv2(x))
        x = self.relu(self.pool(x))

        x = self.drop(self.fc1(x.flatten(start_dim=1)))
        x = self.relu(x)
        
        x = self.drop(self.fc2(x))
        
        return x

    def forward(self, x):
        """
        Forward pass function for the global siamese CNN

        Args:
            x [float32]: input images with dimension Bx2x14x14 (for batch size B)

        Returns:
            [int]: predicted probability ]0,1[
            [float32] : predicted classe by pair, size Bx2x10
        """
        input1 = x[:, 0, :, :].view(-1, 1, 14, 14)  # size Bx1x14x14
        input2 = x[:, 1, :, :].view(-1, 1, 14, 14)
        
        x1 = self.forward_once(input1)  # size Bx1x10
        x2 = self.forward_once(input2)
        
        auxiliary = torch.stack((x1, x2), 1)  # size Bx2x10
        
        output = torch.cat((x1, x2), 1)  # size Bx1x20
        output = self.relu(self.fc3(output))  # size Bx1x10
        output = self.sigmoid(self.fc4(output))  # size Bx1x1
        
        return output.squeeze(), auxiliary
    
    def __str__(self) -> str:
        """Representation"""
        return "Siamese Convolutional Neural Network"
