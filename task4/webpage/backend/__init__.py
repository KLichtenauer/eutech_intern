import os

from flask import Flask, request, jsonify
import torch
from flask_cors import CORS
from torchvision import transforms
from PIL import Image
import random
from CNN_model_training.neural_network import NeuralNetwork

# Initialize Flask and Cors for the Server capabilities.
app = Flask(__name__)
CORS(app)

# Load your PyTorch CNN model
model = NeuralNetwork()
model.load_state_dict(torch.load("../../CNN_model_training/CNN_models/CNN_models3.pt"))
model.eval()

# Path to the folder containing the images
folder_path = '../../fashion_mnist_images'

# Get a list of all files in the folder
all_files = os.listdir(folder_path)

displayed_images = []

def clear_displayed_images():
    displayed_images.clear()

# Randomly select images from a pool of predownloaded MNIST Dataset.
def load_rdm_pictures():
    # Generate three random numbers and store them in a list
    random_numbers = [random.randint(1, 1000) for _ in range(3)]
    # Iterate through the random numbers and select corresponding images.
    for number in random_numbers:
        for file_name in all_files:
            if file_name.endswith(f'image_{number}.jpg'):
                displayed_images.append(os.path.join(folder_path, file_name))


# Define a function to preprocess images before feeding them to the model
def preprocess_image(image):

    # Convert to grayscale
    image = image.convert("L")

    # Adjust image's size and transform to tensor.
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485], std=[0.229]),  # Only one channel for grayscale
    ])
    image = transform(image).unsqueeze(0)
    return image

# API function for evaluating a clicked image.
@app.route('/api/picture', methods=['GET'])
def process_picture():
    # Get the id which is passed with in the url.
    image_id = int(request.args.get('id'))
    # Get image path from array which saves them.
    image_path = displayed_images[image_id - 1]

    # Preprocess the clicked image by opening it with the image path.
    input_image = preprocess_image(Image.open(image_path))

    # Forward pass through the CNN model
    with torch.no_grad():
        output = model(input_image)

    # You can convert the model output to labels or other desired format
    # Here, we'll assume it's a single label
    result = str(output.argmax().item())
    return jsonify(result=result)

# API function for reloading the images.
@app.route('/api/pictures', methods=['GET'])
def load_pics():
    clear_displayed_images()
    load_rdm_pictures()
    return jsonify(selected_images=displayed_images)

# Main function.
if __name__ == '__main__':
    app.run(debug=True)
