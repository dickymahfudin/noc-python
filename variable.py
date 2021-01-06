import os
from dotenv import load_dotenv
from pathlib import Path


print('\n')
# dotenv_path = join(dirname(__file__), '.env')
dotenv_path = Path('.').resolve() / '.env'
# dotenv_path = Path('.').resolve() / 'noc-python' / '.env'
# dotenv_path = "/home/ubuntu/noc-python/.env"
print(dotenv_path)
load_dotenv(dotenv_path)


BASE_URL = os.environ.get("BASE_URL")
PORT_100S_V1 = os.environ.get("PORT_100S_V1")
PORT_APT1 = os.environ.get("PORT_APT1")
PORT_APT2 = os.environ.get("PORT_APT2")
RASPI = os.environ.get("RASPI")
TOKEN_100S_V1 = os.environ.get("TOKEN_100S_V1")
TOKEN_SITE = os.environ.get("TOKEN_SITE")
headerSite = {"Authorization": f"Bearer {TOKEN_SITE}"}
