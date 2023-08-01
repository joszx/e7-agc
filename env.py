# env.py

"""This module defines environment variables and related methods"""


CONFIG = "DEV"
# CONFIG = "PROD"

def isDevMode(): 
        return CONFIG == "DEV"