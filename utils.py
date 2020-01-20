import base64

import cv2
import numpy as np
import grpc

from protos.tensorflow_serving.apis import predict_pb2
from protos.tensorflow_serving.apis import prediction_service_pb2_grpc
from protos.tensorflow.core.framework import (
    tensor_pb2,
    tensor_shape_pb2,
    types_pb2
)


def convert_image(encoded_img, to_rgb=False):

    if isinstance(encoded_img, str):
        b64_decoded_image = base64.b64decode(encoded_img)
    else:
        b64_decoded_image = encoded_img

    img_arr = np.fromstring(b64_decoded_image, np.uint8)

    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.expand_dims(img, axis=-1)
    return img


def grpc_infer(img):

    channel = grpc.insecure_channel("10.5.0.5:8500")
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = "mnist-serving"
    request.model_spec.signature_name = "serving_default"

    if img.ndim == 3:
        img = np.expand_dims(img, axis=0)

    tensor_shape = img.shape
    dims = [tensor_shape_pb2.TensorShapeProto.Dim(size=dim) for dim in tensor_shape]  
    tensor_shape = tensor_shape_pb2.TensorShapeProto(dim=dims)  
    tensor = tensor_pb2.TensorProto(  
                  dtype=types_pb2.DT_FLOAT,
                  tensor_shape=tensor_shape,
                  float_val=img.reshape(-1))
    request.inputs['input_image'].CopyFrom(tensor)  

    try:
        result = stub.Predict(request, 10.0)
        result = result.outputs["y_pred"].float_val
        result = np.array(result).reshape((-1, 10))
        result = np.argmax(result, axis=-1)

        return result
    except Exception as e:
        print(e)
        return None
