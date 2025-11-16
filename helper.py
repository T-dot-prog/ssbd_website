"""
Helper function for SSbd website
"""
import numpy as np
from PIL import Image
import pandas as pd
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

from config import config

from asposeslidescloud import SlidesApi, Configuration

configuration = Configuration()
configuration.app_sid = "4658f1d5-dc13-452c-8229-d69d3f44f9aa"
configuration.app_key = "ab6ea99b2ce188cebc325677e161a650"
configuration.debug = False

slides_api = SlidesApi(configuration)
 
class HelperClass:
    def __init__(self, logo_data_path: str = config.LOGO_PATH, xml_file_path: str = config.XML_PATH):
        self.logo_path = logo_data_path
        self.xml_path = xml_file_path

    def load_logo(self) -> list:
        """Load Logo from Source link"""
        img = Image.open(fp= self.logo_path)

        img_to_array = np.array(img)

        return img_to_array
    
    def load_xlx(self) -> pd.DataFrame:
        """Load Xlxs from Source Link"""
        df = pd.read_excel(self.xml_path)

        return df.to_json()
    
    def convert_into_dict(self) -> dict[str, str]:
        """Convert dataframe into dictionary"""
        data = self.load_xlx()

        data_dict = json.loads(data)

        return data_dict
    
    def name_to_pdf(self, _id: str) -> bytes:
        """Names to pdf bytes"""
        
        with open(f"pdf/{_id}.pdf", "rb") as f:
            data = f.read()

        return data
    

    
    def drivelink_to_image(self, image_id: str) -> bytes:
        """Function to get drivelink to image"""
        import requests

        url = f"https://drive.google.com/uc?export=download&id={image_id}"

        response = requests.get(url)

        return response.content
        

helper = HelperClass()