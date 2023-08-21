import io
from PIL import Image
import onnxruntime
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
import asyncio
import config

app = FastAPI()

class ONNXModelCache:
    def __init__(self, model_path):
        self.model_path = model_path
        self.session = None
    
    def get_session(self):
        if self.session is None:
            self.session = onnxruntime.InferenceSession(self.model_path, 
                                                        providers=['OpenVINOExecutionProvider', 'CPUExecutionProvider'])
        return self.session

model_cache = ONNXModelCache(config.onnx_model_path)  # Replace with your model path

import numpy as np
def process_image(image_data:np.ndarray):
    assert image_data.shape[1:] == (1,28,28) # 这是由onnx模型文件决定的。可用 https://netron.app/ 看到onnx模型的输入大小。
    assert image_data.dtype == np.float32 # 这也是onnx模型要求决定的。
    session = model_cache.get_session()
    
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    input_data = {input_name: image_data}
    result = session.run([output_name], input_data)
    return result[0]

async def process_image_async(image_data:bytes):
    # 这里假设image_data是二进制格式，比如png或者jpg格式。我们需要先解析为内存中的矩阵。
    image_pil = Image.open(io.BytesIO(image_data))
    image_np = np.array(image_pil)
    print(image_np.shape)
    image_np = image_np.reshape(1, 1, 28, 28).astype(np.float32)
    # 这里要做一些torchvision那样的变换，比如resize, normalize等等，可以异步操作。
    # await asyncio.sleep(2)
    result = process_image(image_np)
    return result

@app.post(config.url_route)
async def predict_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_data:bytes = await file.read()
    task_result = await process_image_async(image_data) # 结果是一个np.ndarray
    task_result = str(task_result) # 按照字符串返回。目前是返回所有类别的logits。
    return JSONResponse(content={"result": task_result}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=config.server_port)