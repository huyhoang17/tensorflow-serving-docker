# tensorflow-serving-docker
Tensorflow Serving with Docker / Docker Compose

# Command 

```bash
# step 1
docker-compose build

# step 2 
docker-compose up
```

# Request

- **Input**: base64 image
- HTTP request: `host:8501/v1/models/mnist-serving:predict`
- gRPC request: see [utils.py](utils.py) for more information about how to make gRPC request with protobuf pre-build
