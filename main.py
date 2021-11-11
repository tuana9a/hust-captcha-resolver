import os
import io
import sys
import yaml
import logging
import datetime

from PIL import Image
from flask import Flask, request
from werkzeug.utils import secure_filename

from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor


with open("resource/app.conf.yaml") as f:
    AppConfig = yaml.load(f, Loader=yaml.FullLoader)


def load_model():
    config = AppConfig["vietocr"]
    model_config = Cfg.load_config_from_file(config["weights"]["config"])
    model_config["weights"] = config["weights"]["path"]
    model_config["device"] = config["device_type"]
    model_config["cnn"]["pretrained"] = False
    model = Predictor(model_config)
    return model


def create_server():
    server = Flask(__name__, instance_relative_config=True)
    server.config.from_mapping(MAX_CONTENT_LENGTH=5 * 1024 * 1024)
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    return server


def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in AppConfig["flask"]["allowed_extension"]


model = load_model()
server = create_server()


@server.route("/api/captcha-to-text", methods=["POST"])
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
        result = model.predict(img=image)
        return result

    except:
        print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" + " error when handle image")))
        return "error"


def main():
    bind = AppConfig["server"]["bind"]
    port = os.environ.get("PORT") or AppConfig["server"]["port"]
    server.run(host=bind, port=port, debug=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterupt")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
