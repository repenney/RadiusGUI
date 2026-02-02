# env_loader.py
from dotenv import load_dotenv
import os

# Load .env file next to the EXE
load_dotenv()

def required(var_name):
    """Return the environment variable value or raise an error if missing."""
    val = os.getenv(var_name)
    if val is None or val.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return val

def required_split(var_name):
    """Return a list from a comma-separated environment variable."""
    return required(var_name).split(",")

def required_pair(var1, var2):
    """Return a tuple of two required environment variables."""
    return required(var1), required(var2)





'''
# env_loader.py
from dotenv import load_dotenv
load_dotenv()
'''