import os
from dotenv import load_dotenv
from fake_useragent import UserAgent


load_dotenv()


user_agent = UserAgent()


class Config:
    TMP_DIR = os.getenv("TMP_DIR", "./tmp_html/")
    headers = {
        "access": "*/*",
        "user-agent": user_agent.random
    }
    
