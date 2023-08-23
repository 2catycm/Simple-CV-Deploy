import config
import functools
import onnxruntime

@functools.lru_cache()
def get_model_section():
    return onnxruntime.InferenceSession(config.onnx_model_path, 
                                                        providers=['OpenVINOExecutionProvider', 'CPUExecutionProvider'])
import numpy as np
def softmax( f:np.ndarray):
    # instead: first shift the values of f so that the highest number is 0:
    f -= np.max(f) # f becomes [-666, -333, 0]
    return np.exp(f) / np.sum(np.exp(f))  # safe to do, gives the correct answer

def process_image(image_data:np.ndarray):
    assert image_data.shape[1:] == (1,28,28) # 这是由onnx模型文件决定的。可用 https://netron.app/ 看到onnx模型的输入大小。
    assert image_data.dtype == np.float32 # 这也是onnx模型要求决定的。
    session = get_model_section()
    
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    input_data = {input_name: image_data}
    result = session.run([output_name], input_data)
    result = softmax(result[0])
    
    return result
