import torch
from torch import nn
from torch.utils.data import DataLoader

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

mpl.rcParams['figure.figsize'] = [8.3, 5.1]


class TrainingMetrics:
    """
    Custom class for tracking and plotting training metrics.
    
    Attributes:
        metrics (dict): dictionary that stores metrics on epoch-key
        current (int): current epoch number stored for printing
        run (int): current run when performing trials
        
    Usage:
        1. Define `metrics = TrainingMetrics()` before getting into epoch-loop
        2. Update metrics with `metrics.add_entry(e, l, a, r)`
        3. print(metrics) to display current metrics
    """
    
    def __init__(self):
        """Initialize with empty attributes"""
        self.metrics = {}
        self.current = None
        self.run = None
    
    def __repr__(self) -> str:
        """
        Representation method

        Returns:
            str: representation
        """
        return (f"TrainingMetrics instance of size {len(self.metrics)}")
    
    def __str__(self) -> str:
        """
        Print method

        Returns:
            str: to print when `print(self)` is called
        """
        metric = self.metrics[f"R{self.run}E{self.epoch}"]
        return (f"Epoch {metric['epoch']:02} \t"
                f"Loss {metric['loss']:07.3f} \t"
                f"Accuracy {metric['accuracy'] * 100:06.3f}")
        
    def add_entry(self, epoch: int, loss: float, accuracy: float, run: int = 1) -> None:
        """
        Add entry to metrics

        Args:
            epoch (int): current epoch
            loss (float): loss
            accuracy (float): accuracy
            run (int): the current run number (when doing trials)
        """
        self.run = run
        self.current = epoch
        self.metrics[f"R{run}E{epoch}"] = \
            dict(epoch=epoch, loss=loss, accuracy=accuracy, run=run)
            
    def plot(self):
        """Plot metrics"""
        mf = pd.DataFrame.from_dict(self.metrics, orient='index')
        # mf['epoch'] = mf.index
        
        ax_loss = sns.lineplot(data=mf, x="epoch", y="loss", label='loss',
                               estimator='mean', ci='sd')

        ax_acc = ax_loss.twinx()

        sns.lineplot(data=mf, x="epoch", y="accuracy", label='accuracy',
                     color='r', ax=ax_acc,
                     estimator='mean', ci='sd')

        plt.show()


class TestingMetrics():
    
    def __init__(self, model, data_loader):
        """
        Initiate TestinMetrics instance.

        Args:
            model (nn.Module): model of interest with output (prediction, auxiliary)
            data_loader (DataLoader): data loader with sample structure
                that follows unpacking (input, target, classes)
        """
        self.model = model
        self.loader = data_loader
        self.confusion = dict(true_positive=0, false_negative=0,
                              false_positive=0, true_negative=0)
        self.accuracy = 0.
        self.precision = 0.
        self.recall = 0.
        self.f1_score = 0.
        
        self.compute()
               
    def compute(self):
        
        self.model.eval()
        
        with torch.no_grad():
            for (input, target, _) in self.loader:
                output, _ = self.model(input)
                
                output = (output >= 0.5)
                
                for out, tar in zip(output, target):
                
                    tar = bool(tar)
                    
                    if out and tar:
                        self.confusion['true_positive'] += 1
                    elif not out and not tar:
                        self.confusion['true_negative'] += 1
                    elif out and not tar:
                        self.confusion['false_positive'] += 1
                    elif not out and tar:
                        self.confusion['false_negative'] += 1
        
        self.accuracy = (self.confusion['true_positive'] + self.confusion['true_negative']) \
            / sum(list(self.confusion.values()))
        
        self.precision = self.confusion['true_positive'] \
            / (self.confusion['true_positive'] + self.confusion['false_positive'])
            
        self.recall = self.confusion['true_positive'] \
            / (self.confusion['true_positive'] + self.confusion['false_negative'])
            
        self.f1_score = 2 * self.precision * self.recall / (self.precision + self.recall)
        
    def __str__(self) -> str:
        """
        Print method

        Returns:
            str: to print when `print(self)` is called
        """
        return f"Acc. {self.accuracy * 100:06.3f} | Prec. {self.precision * 100:06.3f} | " \
            f"Rec. {self.accuracy * 100:06.3f} | F1 {self.f1_score * 100:06.3f}"
            
    def plot(self):
        
        mf = pd.DataFrame(
            np.array(list(self.confusion.values())).reshape(2, 2)
        )
        
        mf.columns, mf.index = ['True', 'False'], ['True', 'False']
        
        fig, ax = sns.heatmap(mf, annot=True, cmap='Blues')
        
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Ground Truth')
        

def evaluate_accuracy(model: nn.Module, loader: DataLoader) -> float:
    """
    Computes the classification accuracy of a model.
    Args:
        model (nn.Module): model of interest with output (prediction, auxiliary)
        loader (DataLoader): data loader with sample structure
            that follows unpacking (input, target, classes)
    Returns:
        float: classification accuracy
    """
    
    accuracy = 0.
    counter = 0
    
    model.eval()
    
    with torch.no_grad():
        for (input, target, _) in loader:
            output, _ = model(input)
            
            accuracy += (output >= 0.5) == target
            counter += target.size(0)
                
    return (accuracy.sum() / counter).float().item()
