from sentence_transformers import SentenceTransformer, CrossEncoder
import src.config as config

_models = {}

def load_model(model_name, model_class=SentenceTransformer):

    key = (model_class, model_name)

    if key not in _models:
        _models[key] = model_class(model_name)

    return _models[key]