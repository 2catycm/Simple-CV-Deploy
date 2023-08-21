import io
from PIL import Image
import onnxruntime
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
import asyncio

app = FastAPI()

class ONNXModelCache:
    def __init__(self, model_path):
        self.model_path = model_path
        self.session = None
    
    def get_session(self):
        if self.session is None:
            self.session = onnxruntime.InferenceSession(self.model_path)
        return self.session

model_cache = ONNXModelCache("path_to_your_model.onnx")  # Replace with your model path

def process_image(image_data):
    session = model_cache.get_session()
    
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    input_data = {input_name: image_data}
    result = session.run([output_name], input_data)
    return result[0]

async def process_image_async(image_data):
    result = process_image(image_data)
    # Simulate some asynchronous processing
    # await asyncio.sleep(2)
    return result

@app.post("/predict/")
async def predict_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_data = await file.read()
    task_result = await process_image_async(image_data)
    return JSONResponse(content={"result": task_result}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)