import io
import logging
import datetime

from PIL import Image
from ocr import captcha2text
from flask import Flask, request
from configs import AppConfig
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(MAX_CONTENT_LENGTH=5 * 1024 * 1024)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


def is_allowed_extension(filename):
    allowed_extensions = AppConfig["flask"]["allowed_extensions"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@app.route("/", methods=["GET"])
def index():
    return "hello world"


@app.route("/api/captcha-to-text", methods=["POST"])
def captcha_to_text():
    if "file" not in request.files:
        return "no file upload"

    file = request.files["file"]

    if not file:
        return "no file upload"

    filename = secure_filename(file.filename)

    if not is_allowed_extension(filename):
        return "not allowed " + filename

    try:
        buffers = file.stream._file.getvalue()
        image = Image.open(io.BytesIO(buffers))
        result = captcha2text.predict(img=image)
        return result

    except:
        pattern = "%Y-%m-%d %H:%M:%S" + " error when handle image"
        now = datetime.datetime.now().strftime(pattern)
        print(str(now))
        return "error"
