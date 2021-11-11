import yaml

file = open("resource/app.conf.yaml")
AppConfig = yaml.load(file, Loader=yaml.FullLoader)
