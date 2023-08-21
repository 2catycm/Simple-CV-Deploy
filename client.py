import requests

def send_image_to_server(image_path):
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        response = requests.post("http://localhost:8000/predict/", files=files)
        return response

if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"  # Replace with your image path
    response = send_image_to_server(image_path)
    print("Response:", response.status_code, response.json())
