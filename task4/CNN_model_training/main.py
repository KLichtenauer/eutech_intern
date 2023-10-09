# Import necessary libraries
import torch
from torch import nn
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda
from torch.utils.data import DataLoader
import logging

# Import custom modules
from neural_network import NeuralNetwork  # Import your custom neural network module
from train_test import train_loop, test_loop  # Import your custom training and testing loops

# Define a class for training a Convolutional Neural Network (CNN) on Fashion MNIST dataset
class MNIST_Trainer:
    # Configure logging to save results and parameters to a log file
    logging.basicConfig(filename='../parameters_and_results.log', level=logging.INFO,
                        format='%(message)s')

    def __init__(self, batch_size=64, learning_rate=1.5e-3, epochs=40):
        """
        Initialize the FashionMNISTTrainer class.

        Parameters:
            - batch_size: Batch size for training and testing.
            - learning_rate: Learning rate for the optimizer.
            - epochs: Number of training epochs.
        """
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs

        # Log hyperparameters for reference
        logging.info(f"Hyperparameters: batch_size={batch_size}, learning_rate={learning_rate}, epochs={epochs}")

    def load_data(self):
        """
        Load the Fashion MNIST dataset and create data loaders for training and testing.
        """
        # Define transformations for the dataset
        transform = ToTensor()
        target_transform = Lambda(lambda y: torch.zeros(10, dtype=torch.float).scatter_(0, torch.tensor(y), value=1))

        # Create training and testing datasets
        self.training_data = datasets.MNIST(
            root="../data",
            train=True,
            download=False,  # Set to True to download the dataset if not available locally
            transform=transform,
            target_transform=target_transform
        )

        self.test_data = datasets.MNIST(
            root="../data",
            train=False,
            download=False,  # Set to True to download the dataset if not available locally
            transform=transform,
            target_transform=target_transform
        )

        # Create data loaders for training and testing
        self.train_dataloader = DataLoader(self.training_data, batch_size=self.batch_size, shuffle=True)
        self.test_dataloader = DataLoader(self.test_data, batch_size=self.batch_size, shuffle=True)

    def train(self):
        """
        Train the Convolutional Neural Network (CNN) on the Fashion MNIST dataset.
        """
        # Check if GPU is available, otherwise use CPU
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        # Create an instance of the custom NeuralNetwork model and move it to the chosen device
        self.model = NeuralNetwork().to(device)

        # Define loss function and optimizer
        loss_fn = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)

        # Training loop
        for t in range(self.epochs):
            print(f"Epoch {t + 1}\n-------------------------------")
            train_loop(self.train_dataloader, self.model, loss_fn, optimizer)
            test_loop(self.test_dataloader, self.model, loss_fn)
        print("Training Done!")

if __name__ == "__main__":
    # Create an instance of the FashionMNISTTrainer class
    trainer = MNIST_Trainer()

    # Load the Fashion MNIST dataset
    trainer.load_data()

    # Train the CNN model
    trainer.train()

    # Save the trained model to a file
    version = 3
    torch.save(trainer.model.state_dict(), f'CNN_models/CNN_models{version}.pt')
