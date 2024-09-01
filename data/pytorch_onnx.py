#%%
import torch
from onnx2torch import convert
import onnx
onnx_model_path = "./mnist.onnx"
onnx_model = onnx.load(onnx_model_path)
# torch_model = convert(onnx_model)
# torch_model
# %%
from onnx_pytorch import code_gen
code_gen.gen(onnx_model_path, "mnist")
# %%
