import os
import dotenv
import yaml
import traceback
import torch
import uvicorn

from PIL import Image
from fastapi import FastAPI, Request, UploadFile
from vietocr.tool.config import Cfg
from pydantic import BaseModel
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor as _Predictor
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

dotenv.load_dotenv(dotenv.find_dotenv())

PORT = os.getenv("PORT") or 5000
BIND = os.getenv("BIND") or "0.0.0.0"
DEVICE = os.getenv("DEVICE") or "cpu"
DEBUG = True if os.getenv("DEBUG") else False
WEIGHT_CONF_PATH = os.getenv("WEIGHT_CONF_PATH") or "weights.yaml"
SECRET = os.getenv("SECRET")
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5mb
SUPPORTED_DEVICES = [
    "cpu", "cuda", "cuda:0", "xpu", "mkldnn", "opengl", "opencl", "ideep",
    "hip", "msnpu", "xla", "vulkan"
]
CUDA_DEVICES = ["cuda", "cuda:0"]


class Predictor:

    def __init__(self) -> None:
        self.cfg = None
        self.predictor = None

    def predict(self, img) -> str:
        return self.predictor.predict(img)

    def load(self):
        self.predictor = _Predictor(self.cfg)
        return self.predictor

    def set_cfg(self, cfg: Cfg):
        self.cfg = cfg

    def change_device(self, device: str):
        self.cfg["device"] = device


predictor = Predictor()
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(
        ".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_allowed_device(device):
    return device in SUPPORTED_DEVICES


with open(WEIGHT_CONF_PATH) as f:
    predictor.set_cfg(Cfg(yaml.safe_load(f)))
    predictor.change_device(DEVICE)
    predictor.load()


class ChangeDeviceRequest(BaseModel):
    device: str
    secret: str


@app.get("/")
def hello_world():
    return "hello world"


@app.post("/")
@limiter.limit("5/minute")
# request: Request argument is a must for ratelimit to work
def upload_image_to_predict(request: Request, file: UploadFile):
    # TODO: max file upload
    if not file:
        return "file is empty"
    filename = file.filename
    if not is_allowed_extension(filename):
        return "extension is not allowed: " + filename
    result = None
    try:
        image = Image.open(file.file)
        result = predictor.predict(img=image)
    except Exception as err:
        result = f"Error: {err} {change_device.__name__}(): {traceback.format_exc()}"
    return result


@app.post("/change_device")
@limiter.limit("5/minute")
# request: Request argument is a must for ratelimit to work
def change_device(request: Request, body: ChangeDeviceRequest):
    # TODO: rate limit change device
    try:
        device = body.device
        if not is_allowed_device(device):
            return "device is not allowed"
        if device in CUDA_DEVICES:
            if not torch.cuda.is_available():
                return "cuda device is not available"
        secret = body.secret
        if secret != SECRET:
            return "secret is not correct"
        predictor.change_device(device)
        predictor.load()
        return device
    except RuntimeError as err1:
        return f"Error: {err1} {change_device.__name__}(): {traceback.format_exc()}"
    except Exception as err2:
        return f"Error: {err2} {change_device.__name__}(): {traceback.format_exc()}"


def main():
    uvicorn.run(app, host=BIND, port=int(PORT))


if __name__ == "__main__":
    main()
