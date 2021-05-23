import torch

class Optimizer(object):
    """
    Optimization base class
    The optimizer update the parameters after the gradient is calculated through backward propagation
    The parameters are then updated after each sample.
    """
    def step(self, *args):
        """
        Gradient Descent parameter update
        """
        raise NotImplementedError


class SGD(Optimizer):
    """
    Parameters are obtained with model.param() with model a pytorch network
    p[0] is the parameter, p[1] is the respective gradient

    Attributes:
    parameters: parameter of the network model, obtained with model.param()
    lr: learning rate
    momentum: momentum coefficient 
    """
    def __init__(self, parameters, lr, momentum=0):
    
        self.parameters = parameters
        self.lr = lr
        self.momentum = momentum
        self.v = self.zero_velocity()

    def zero_velocity(self):
        """
        Initialize the velocity vector as zeros to match with parameter shape
        """
        v = []
        for p in self.parameters:
            v.append(torch.zeros_like(p[0]))
        return v
    
    def step(self):
        """
        The SGD momentum update parameters with regard to Sutskever definition
        """
        for i, p in enumerate(self.parameters):
            self.v[i] = self.momentum * self.v[i] + self.lr * p[1]
            p[0] = p[0] - self.v[i]

