import os
import numpy as np
from PIL import Image
import torch
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda

# !!!!!! This class does only needs to be executed once and everytime you want to change up the 1000 images for the website. !!!!!

# Loads the MNIST dataset making it accessible.
training_data = datasets.MNIST(
            root="data",
            train=True,
            download=False,
            transform=ToTensor(),
            target_transform=Lambda(lambda y: torch.zeros(10, dtype=torch.float).scatter_(0, torch.tensor(y), value=1))
        )

images = training_data.data.numpy()

# Create a directory to save the JPEG images
output_dir = "../../fashion_mnist_images"
os.makedirs(output_dir, exist_ok=True)

# Loop through the images and save them as JPEG
for i, image in enumerate(images):
    if i < 1000:
        image = (image * 255).astype(np.uint8)  # Convert to 8-bit integer
        image = Image.fromarray(image, mode="L")  # Create grayscale image
        image_path = os.path.join(output_dir, f"image_{i}.jpg")
        image.save(image_path)


print(f"Saved {len(images)} images to {output_dir}")


