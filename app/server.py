from fastapi import FastAPI, WebSocket
import numpy as np

import config
app = FastAPI()

import ai
# WebSocket route
@app.websocket(config.url_route)
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        image_data = await websocket.receive_bytes()
        image_array = np.frombuffer(image_data, dtype=np.float32).reshape((1, 1, 28, 28))
        
        # Replace this with your image processing logic
        # Here we just send a simple response for demonstration
        # response_text = f"Received image with shape {image_array.shape}"
        res = ai.process_image(image_array)
        res = res[0]
        y_pred = np.argmax(res)
        y_pred_prob = res[y_pred]
        res = f"{y_pred} with probability {y_pred_prob*100:.2f}%"
        await websocket.send_text(res)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=config.server_port)
