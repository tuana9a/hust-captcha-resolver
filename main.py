import os
import dotenv
import yaml
import traceback
import uvicorn

from PIL import Image
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import PlainTextResponse
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

dotenv.load_dotenv(dotenv.find_dotenv())

PORT = os.getenv("PORT") or 8080
BIND = os.getenv("BIND") or "127.0.0.1"
DEVICE = os.getenv("DEVICE") or "cpu"
DEBUG = True if os.getenv("DEBUG") else False
WEIGHT_CONF_PATH = os.getenv("WEIGHT_CONF_PATH") or "weights.yaml"
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
SUPPORTED_DEVICES = [
    "cpu", "cuda", "cuda:0", "xpu", "mkldnn", "opengl", "opencl", "ideep",
    "hip", "msnpu", "xla", "vulkan"
]
CUDA_DEVICES = ["cuda", "cuda:0"]
UPLOAD_RATE_LIMIT = os.getenv("UPLOAD_RATE_LIMIT") or "60/minute"


class DITO: # preDIcTOr
    def __init__(self, cfg: Cfg) -> None:
        self.cfg = cfg
        self.predictor = Predictor(self.cfg)

    def predict(self, img) -> str:
        return self.predictor.predict(img)


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def is_allowed_extension(filename):
    if not "." in filename:
        return False
    if not filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        return False
    return True


def is_allowed_device(device):
    return device in SUPPORTED_DEVICES


with open(WEIGHT_CONF_PATH) as f:
    cfg = Cfg(yaml.safe_load(f))
    if not is_allowed_device(DEVICE):
        raise ValueError(DEVICE)
    cfg["device"] = DEVICE
    dito = DITO(cfg)


@app.get("/", response_class=PlainTextResponse)
def hello_world():
    return "hello world"


@app.post("/", response_class=PlainTextResponse)
@limiter.limit(UPLOAD_RATE_LIMIT)
# request: Request argument is a must for ratelimit to work
def predict(request: Request, file: UploadFile):
    # TODO: max file upload
    if not file:
        return "file is empty"
    filename = file.filename
    if not is_allowed_extension(filename):
        return "extension is not allowed: " + filename
    result = None
    try:
        image = Image.open(file.file)
        result = dito.predict(img=image)
    except Exception as err:
        result = f"Error: {err} {predict.__name__}(): {traceback.format_exc()}"
    return result


def main():
    uvicorn.run(app, host=BIND, port=int(PORT))


if __name__ == "__main__":
    main()
