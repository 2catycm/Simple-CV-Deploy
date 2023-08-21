import os
import requests
import gzip
import numpy as np

# Define the URLs for MNIST dataset
urls = {
    "train-images-idx3-ubyte": "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte": "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte": "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte": "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
}

# Create a directory for test data if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

def download_mnist_data():
    for key, url in urls.items():
        response = requests.get(url)
        with open(f"data/{key}.gz", "wb") as f:
            f.write(response.content)
    import os
    # 解压gz
    for key, url in urls.items():
        os.system(f"gzip -d data/{key}.gz")
    
    print("MNIST data downloaded.")

import os
from mnist import MNIST
from PIL import Image
def extract_mnist_data():
    # Load MNIST dataset
    mndata = MNIST("data")  # Replace with the path to your MNIST data folder
    images, _ = mndata.load_testing()

    # Save a few MNIST images to the test_data folder
    num_images_to_save = 5
    for i in range(num_images_to_save):
        image = images[i]
        image_pil = Image.fromarray(np.array(image).reshape(28, 28).astype(np.uint8), mode="L")
        image_path = f"data/mnist_image_{i}.png"
        image_pil.save(image_path)
    print("MNIST images saved to test_data folder.")


def main():
    download_mnist_data()
    extract_mnist_data()

if __name__ == "__main__":
    main()
