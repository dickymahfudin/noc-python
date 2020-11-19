import os
from os.path import join, dirname
from dotenv import load_dotenv

print('\n')
# dotenv_path = join(dirname(__file__), '.env')
dotenv_path = join(os.getcwd(), '.env')
print(dotenv_path)
load_dotenv(dotenv_path)

BASE_URL = os.environ.get("BASE_URL")
print(BASE_URL)
