import unittest
from fastapi.testclient import TestClient
from app.server import app

class TestPredictEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_predict_image(self):
        with open("path_to_test_image.jpg", "rb") as image_file:
            files = {"file": image_file}
            response = self.client.post("/predict/", files=files)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("result" in response.json())

if __name__ == "__main__":
    unittest.main()
