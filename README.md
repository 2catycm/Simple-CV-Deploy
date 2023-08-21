# 图片识别服务器和客户端示例 Simple-CV-Deploy

这是一个使用 FastAPI 和 Python 异步机制实现的高性能图片识别服务器和客户端示例。服务器可以异步处理图片识别请求，并返回处理结果，而客户端可以发送图片到服务器并获取处理结果。

## 服务器端

### 安装依赖

确保你的系统上安装了 Python 3.6+，然后使用以下命令安装依赖：

```bash
pip install -r requirements.txt
# 或者使用虚拟环境+make
make setup 
```
其中，
onnxruntime 默认使用 CPU_EXECUTION_PROVIDER。
要想使用Intel的OpenVINO，可以使用
```bash  
pip uninstall onnxruntime
pip install onnxruntime-openvino
```

### 启动服务器

在服务器端文件夹中运行以下命令启动服务器：

```bash
python app/server.py
# 或者使用虚拟环境+make
make run-server
```

## 客户端


### 运行客户端

在客户端文件夹中运行以下命令以运行客户端：

```bash
python app/client.py
# 或者使用虚拟环境+make
make run-client
```

客户端将会发送图片给服务器并获取处理结果。

## 注意事项

- 在实际使用中，你需要替换`app/config.py`中的 的一些配置，来指定onnx模型、端口号等。
- 这只是一个基础示例，你可以根据实际需求进行扩展和优化。



## 使用 Dockerfile 构建和运行 Simple-CV-Deploy 

Simple-CV-Deploy 是一个 FastAPI 应用程序，可以使用 Dockerfile 构建和运行在 Docker 容器中。该示例使用 Docker 来封装 FastAPI 应用程序以及相关依赖。


### 构建 Docker 镜像

1. 确保已经安装了 Docker。如果没有安装，请根据你的操作系统进行安装。

2. 在与 `Dockerfile` 和 `requirements.txt` 相同的目录中，打开终端。

3. 运行以下命令以构建 Docker 镜像。将 `my-fastapi-app` 替换为你喜欢的镜像名称。

   ```bash
   docker build -t my-fastapi-app .
   ```

### 运行 Docker 容器

1. 在构建成功后，运行以下命令以在 Docker 容器中运行 FastAPI 应用程序。将端口映射到主机的端口，例如将容器的 8000 端口映射到主机的 8000 端口。

   ```bash
   docker run -p 8000:8000 my-fastapi-app
   ```

### 访问 FastAPI 应用

1. 在运行容器后，你可以通过浏览器或者命令行工具访问 FastAPI 应用。在浏览器中，访问 `http://localhost:8000` 来访问应用。

2. 在命令行中，你也可以使用工具如 `curl` 或者 `httpie` 来发送 HTTP 请求，例如：

   ```bash
   curl http://localhost:8000/predict/ -F "file=@path_to_your_image.jpg"
   ```

### 注意事项

- 确保你的应用程序的相关路径和配置正确。例如，确保 `path_to_your_model.onnx` 和 `path_to_your_image.jpg` 的路径设置正确。
- 此 README 仅为简单的演示，你可能需要根据实际情况进行适当的调整和配置。

