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
import os

from config import config

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
    
    def name_to_pptx_to_pdf(self, name: str) -> bytes:
        """
        A function for creating a certificate
        
        Args:
            name: (str) 
        Returns:
            - None
        """
        prs = Presentation(config.TEMPLATE_PPTX)
        slide = prs.slides[0]

        left = Inches(1.9)
        top = Inches(3.13)
        width = Inches(7.34)
        height = Inches(0.85)

        textbox = slide.shapes.add_textbox(left, top, width, height)
        tf = textbox.text_frame        

        p = tf.add_paragraph()
        p.text = name   # participant name
        p.font.name = "Slight"               # or "Times New Roman"
        p.font.italic = False
        p.font.size = Pt(20)
        p.alignment = PP_ALIGN.CENTER # To Center the text 

        PPTX_FILE = "sample.pptx"
        PDF_FILE = "sample.pdf"
        SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

        #Save to a created file 
        prs.save(PPTX_FILE)

        # convert pptx -> pdf file 
        import subprocess

        subprocess.run([
    SOFFICE_PATH, "--headless", "--convert-to", "pdf", PPTX_FILE, "--outdir", "."
], check=True)
        
        with open(PDF_FILE, "rb") as file:
            pdf_bytes = file.read()

        return pdf_bytes

helper = HelperClass()