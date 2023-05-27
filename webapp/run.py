import os
import pickle
from fashion_clip.fashion_clip import FashionCLIP
import pandas as pd
import numpy as np
from PIL import Image

os.environ["TRANSFORMERS_CACHE"] = "/workspace/cache_data"
os.environ["HF_HOME"] = "/workspace/cache_data"
EMBEDDING_PATH = "/workspace/cache_data/image_embeddings.pkl"

def load_fclip():
    """
    Load the fashion clip model.
    We are going to cache this function to avoid having to load the model every time.

    :return:
    """
    fclip = FashionCLIP('fashion-clip')
    return fclip


def load_or_create_embeddings(fclip):
    """
    Load the image embeddings from the cache or create them if they don't exist.

    :return:
    """
    if os.path.exists(EMBEDDING_PATH):
        with open(EMBEDDING_PATH, "rb") as f:
            image_embeddings = pickle.load(f)
    else:
        subset = pd.read_csv("/workspace/cache_data/new_dataset/subset.csv")

        # add path to images
        images = [f"/workspace/cache_data/new_dataset/{k}.jpg" for k in subset["article_id"].tolist()]
        image_embeddings = fclip.encode_images(images, 32)
        image_embeddings = image_embeddings / np.linalg.norm(image_embeddings, ord=2, axis=-1, keepdims=True)

        with open(EMBEDDING_PATH, "wb") as f:
            pickle.dump(image_embeddings, f)

    return image_embeddings

def search_image(**inputs):

    fclip = load_fclip()
    subset = pd.read_csv("/workspace/cache_data/new_dataset/subset.csv")
    image_embeddings = load_or_create_embeddings(fclip)

    query = inputs["query"]

    text_embedding = fclip.encode_text([query], 32)[0]
    text_embedding = text_embedding/np.linalg.norm(text_embedding)

    id_of_matched_object = np.argmax(text_embedding.dot(image_embeddings.T))
    found_object = subset["article_id"].iloc[id_of_matched_object].tolist()

    image = Image.open("/workspace/cache_data/new_dataset/" + str(found_object) + ".jpg")

    image.save("output.png")
