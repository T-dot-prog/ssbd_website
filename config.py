import os
from pydantic_settings import BaseSettings

from typing_extensions import Optional
import warnings

warnings.filterwarnings("ignore")


class Config(BaseSettings):
    "Application Settings and Configuration"

    LOGO_PATH: str = "data/ssbd_logo.jpg"
    XML_PATH: str = "data/Profile data.xlsx"

    COURSE_TITLE: str = "ANSYS Fluent Course (CFD & Heat Transfer)"
    COURSE_DURATION: str = "17th October,2025 to 13th November,2025; 12 sessions"

    REDIS_URL: str = os.getenv("REDIS_URL")
    
    KEY_STR: str = "ID"
    OTHER_INFO: list = ["Name ", "Email Address"]

    TEMPLATE_PPTX: str = "pptx_src/Certificate.pptx"


config = Config()
