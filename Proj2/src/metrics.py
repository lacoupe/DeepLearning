from module import Module
from torch import Tensor


def evaluate_accuracy(model: Module, in_: Tensor, target: Tensor) -> float:
    """
    Computes the classification accuracy of a model.
    Args:
        model (Module): model of interest with output (prediction, auxiliary)
        input (Tensor): input data
        target (Tensor): target data
    Returns:
        float: classification accuracy
    """
    
    model.eval()
    
    output = model(in_)
    
    return (output == target).float().sum(1) / target.size(0)
