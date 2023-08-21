# 图片识别服务器和客户端示例 Simple-CV-Deploy

这是一个使用 FastAPI 和 Python 异步机制实现的高性能图片识别服务器和客户端示例。服务器可以异步处理图片识别请求，并返回处理结果，而客户端可以发送图片到服务器并获取处理结果。

## 服务器端

### 安装依赖

确保你的系统上安装了 Python 3.6+，然后使用以下命令安装依赖：

```bash
pip install fastapi onnxruntime uvicorn
```

### 启动服务器

在服务器端文件夹中运行以下命令启动服务器：

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

其中，`server` 是服务器端代码所在的文件名，`app` 是 FastAPI 实例的名称。

## 客户端

### 安装依赖

确保你的系统上安装了 Python 3.6+，然后使用以下命令安装依赖：

```bash
pip install requests
```

### 运行客户端

在客户端文件夹中运行以下命令以运行客户端：

```bash
python client.py
```

客户端将会发送图片给服务器并获取处理结果。

## 注意事项

- 在实际使用中，你需要替换 `path_to_your_model.onnx` 和 `path_to_your_image.jpg` 分别为你的模型路径和图片路径。
- 这只是一个基础示例，你可以根据实际需求进行扩展和优化。

---

请确保根据实际情况修改路径、端口等信息，并适当添加更多的细节和说明。这个 README 文件将帮助其他人了解如何运行和使用你的服务器和客户端应用。