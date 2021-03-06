from torch import Tensor
from .module import Module


class BCELoss(Module):
    """
    Binary Cross Entropy Loss
    """
  
    def forward(self, prediction: Tensor, target: Tensor) -> Tensor:
        """
        Forward pass:

        Arguments
        Prediction (torch.Tensor): Predicted output of the network
        Target (torch.Tensor): Target of the network

        Returns:
        Binary Cross entropy loss (torch.tensor)
        """
        self.prediction = prediction.view(-1)
        self.target = target

        if (prediction < 0).any():
            raise Exception('Error: Binary Cross Entropy Loss takes positive values')

        # Computing the BCEloss
        loss = target.mul(self.prediction.log())
        loss += (1 - self.target).mul((1 - self.prediction).log())

        return -loss.mean()

    def backward(self) -> Tensor:
        """
        Back Propagation: back ward pass of the derivative of the cross entropy function
        """
        grad = self.target.div(self.prediction)
        grad -= (1 - self.target).div(1 - self.prediction)

        return -grad.unsqueeze(1)
    
    def sigmoid(self):
        """
        Sigmoid of the predicted value that returns a
        probability of belonging either to class 0 or 1
        """
        activated = 1 / (1 + (-self.prediction).exp())
        return activated
    
    def d_sigmoid(self):
        """
        Derivative of sigmoid funciton
        """
        return self.sigmoid().mul(1 - self.sigmoid())
