from setuptools import setup, find_packages

setup(
    name="SSBD Profile verification Site",
    version="0.0.1",
    description="A Streamlit web application for users in the SSBD Course",
    author="Tahasin Islam",
    author_email="tahasinahoni2@gmail.com",
    packages=find_packages(),
    install_requires=["streamlit", "redis", "openpyxl", "pydantic_settings", "python-pptx", "streamlit[pdf]"],
    entry_points={"console_scripts": ["ssbd_website=ssbd_website.__main__:main"]},
    include_package_data=True,
)
