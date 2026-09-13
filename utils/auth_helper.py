import os 
from dotenv import load_dotenv

load_dotenv()
VALID_TOKEN  = os.getenv("SECRET_TOKEN")

def verify_token(token):
    if token != VALID_TOKEN:
        return False
    return True
