import requests
import config
def send_image_to_server(image_path):
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        response = requests.post(f"http://localhost:{config.server_port}{config.url_route}", files=files)
        return response

if __name__ == "__main__":
    image_path = "data/mnist_image_0.png"  # Replace with your image path
    response = send_image_to_server(image_path)
    print("Response:", response.status_code, response.json())
