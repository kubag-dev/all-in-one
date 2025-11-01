import os

from dotenv import load_dotenv


load_dotenv()

DEBUG_MODE = os.getenv("DEBUG")
