"""
Sales Register Analysis Tool
----------------------------

A Streamlit application for analyzing sales register data with SA 520 procedures.
Designed for audit professionals to perform trend analysis and sampling.
"""

__version__ = '0.1.0'
__author__ = 'Nishanth'
__email__ = 'nishanth@varmaandvarma.com'

# Import main components to make them available when importing the package
from .app import main

# Define what's available when using "from sales_register_analysis import *"
__all__ = ['main']
