import os
import sys

from app import app
from configs import AppConfig


def main():
    bind = AppConfig["server"]["bind"]
    port = os.environ.get("PORT") or AppConfig["server"]["port"]
    app.run(host=bind, port=port, debug=False)


if __name__ == "__main__":
    try:
        main()
    except:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
