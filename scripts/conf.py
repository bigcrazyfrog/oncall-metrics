import logging
from os import PathLike

# Settings file
# Set your own configuration here

# Path to yaml file
YAML_FILE_PATH: str | PathLike[str] = "data.yaml"

# Host and port of server
HOST: str = "localhost"
PORT: str = "8080"

# We use http because debug mode is assumed
BASE_URL: str = f"http://{HOST}:{PORT}"

# Admin user for authorization
USER: str = "root"
PASSWORD: str = "root"

# Logger settings
logging.basicConfig(
    level=logging.INFO,
    filename="oncall_log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)
