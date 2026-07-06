import os
import src.config as config

os.environ["HF_HOME"] = config.HF_CACHE

if config.HF_ENDPOINT:
    os.environ["HF_ENDPOINT"] = config.HF_ENDPOINT

if config.HF_OFFLINE:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"