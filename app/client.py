import asyncio
import websockets
import numpy as np
import config
from  pathlib import Path
from PIL import Image
import time 
import itertools
import tqdm
import aiofiles
import io

this_file = Path(__file__).resolve()
this_directory = this_file.parent
data_directory = this_directory.parent / "data"

import mnist
mndata = mnist.MNIST(data_directory)  # Replace with the path to your MNIST data folder
images, labels = mndata.load_testing()

import os
rank = int(os.environ.get('rank', '0'))

async def load_image_bytes(image_path):
    async with aiofiles.open(image_path, "rb") as f:
        image_data = await f.read()
    return image_data

async def load_pil(image_data):
    return Image.open(io.BytesIO(image_data)).convert("L").resize(28, 28)  # Convert to grayscale
    
async def preprocess_image(image_np:np.ndarray):
    image_np = image_np.astype(np.float32).reshape((1, 1, 28, 28))  # Resize to 28x28
    image_np = image_np / 255.0  # Normalize pixel values
    return image_np


async def send_image():
    uri = f"ws://localhost:{config.server_port}{config.url_route}"
    start_time = time.time() 
    async with websockets.connect(uri) as websocket:
        bar = tqdm.tqdm(itertools.count(1))
        for i in bar:
            # Replace this with your image data preparation logic
            # image_data = np.random.random((28, 28))  # Example random image data
            # num = np.random.randint(1, 5)
            # image_data = Image.open(data_directory / f"mnist_image_{int(num)}.png")
            # print(image_data.size)
            
            image_data = images[i%len(images)]
            image_data = np.array(image_data)
            image_data = await preprocess_image(image_data)
            # print(image_data.shape)
            label = labels[i%len(images)]
            
            await websocket.send(image_data.tobytes())

            result = await websocket.recv()
            # print(f"Received result: {result}")
            # await asyncio.sleep(5)  # Send image every 5 seconds

            # suppose_fps = 10
            # suppose_fps = 100
            # suppose_fps = 200
            # suppose_fps = 400
            # suppose_fps = 800
            # suppose_fps = 1000
            # suppose_fps = 10000
            wall_time = time.time() - start_time
            # if i%suppose_fps == 0:
            if i%(int(i/wall_time)) == 0:
                bar.set_postfix({"latency": f"{wall_time/i *1000:.4f} ms", 
                                "fps": f"{i/wall_time:.4f}", 
                                #  "expected_fps": f"{suppose_fps}", 
                                #  "utilization": f"{i/wall_time/suppose_fps*100:.2f} %",
                                "y_pred": result, 
                                "y_true": label, 
                                "rank":f"{rank}"})
            # await asyncio.sleep(1/suppose_fps)  # Send image every 5 seconds
async def main():
    # wait_time = 1
    # wait_time = 4
    wait_time = 10
    while True:
        try:
           await send_image()
        except websockets.ConnectionClosedError:
            print("Connection closed, attempting to reconnect...")
            await asyncio.sleep(wait_time)  # Wait before attempting to reconnect
        except ConnectionRefusedError:
            print("Connection refused, attempting to reconnect...")
            await asyncio.sleep(wait_time)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
