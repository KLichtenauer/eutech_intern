import torch.nn as nn


class NeuralNetwork(nn.Module):
    def __init__(self):
        """
        Initialize a Convolutional Neural Network (CNN) model for image classification.

        The network consists of two main parts:
        1. Convolutional Stack: A sequence of convolutional and pooling layers for feature extraction.
        2. Fully Connected Stack: A sequence of fully connected layers for classification.

        The architecture is designed for image classification tasks.

        """
        super().__init__()

        # Convolutional Stack
        self.conv_stack = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # Input channels: 1, Output channels: 32
            nn.ReLU(),  # ReLU activation function
            nn.MaxPool2d(2),  # Max pooling layer with a kernel size of 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # Input channels: 32, Output channels: 64
            nn.ReLU(),  # ReLU activation function
            nn.MaxPool2d(2)  # Max pooling layer with a kernel size of 2
        )

        # Fully Connected Stack
        self.fc_stack = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),  # Adjust the input size based on the output size of the last conv layer
            nn.ReLU(),  # ReLU activation function
            nn.Linear(128, 10),  # Output layer with 10 classes (for classification)
        )

    def forward(self, x):
        """
        Forward pass through the neural network.

        Parameters:
            - x: Input data (images) with shape (batch_size, channels, height, width).

        Returns:
            - logits: Raw scores (logits) for each class.
        """
        # Pass the input through the convolutional stack
        x = self.conv_stack(x)

        # Flatten the output for the fully connected layers
        x = x.view(x.size(0), -1)

        # Pass through the fully connected stack to get logits
        logits = self.fc_stack(x)

        return logits
