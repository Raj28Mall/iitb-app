from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH")

config= Config()

#validator
#cleaner
#read files
#upload files