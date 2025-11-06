from argparse import OPTIONAL
from pydantic_settings import BaseSettings

from typing_extensions import Optional
import warnings

warnings.filterwarnings("ignore")


class Config(BaseSettings):
    "Application Settings and Configuration"

    LOGO_PATH: str = "F:/ssbd_logo.jpg"
    XML_PATH: str = "data/Profile data.xlsx"

    COURSE_TITLE: str = "ANSYS Fluent Course (CFD & Heat Transfer)"
    COURSE_DURATION: str = "17th October,2025 to 13th November,2025; 12 sessions"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_TTL: int = 3600  # 1 hour default TTL

    KEY_STR: str = "ID"
    OTHER_INFO: list = ["Name ", "Email Address"]

    TEMPLATE_PPTX: str = "F:/Certificate.pptx"


config = Config()
