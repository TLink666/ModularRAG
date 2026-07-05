from src.config import *
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = HF_CACHE
from sentence_transformers import SentenceTransformer, CrossEncoder

_models = {}

def load_model(model_name, model_class=SentenceTransformer):

    key = (model_class, model_name)

    if key not in _models:
        _models[key] = model_class(model_name)

    return _models[key]