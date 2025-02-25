from setuptools import setup, find_packages

setup(
    name="sales_register_analysis",
    version="0.1.0",
    author="Nishanth",
    author_email="nishanth@varmaandvarma.com",
    description="A Streamlit application for sales register analysis with SA 520 procedures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # Add your repository URL here
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.22.0",
        "pandas>=1.5.0",
        "plotly>=5.14.0",
        "numpy>=1.23.0",
    ],
    entry_points={
        "console_scripts": [
            "sales-analysis=sales_register_analysis.app:main",
        ],
    },
)
