from configs import AppConfig
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

config = AppConfig["vietocr"]
model_config = Cfg.load_config_from_file(config["weights"]["config"])
model_config["weights"] = config["weights"]["path"]
model_config["device"] = config["device_type"]
model_config["cnn"]["pretrained"] = False
captcha2text = Predictor(model_config)
