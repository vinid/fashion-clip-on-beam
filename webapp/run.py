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
        # first we get all the paths of the images
        images = [f"/workspace/cache_data/new_dataset/{k}.jpg" for k in subset["article_id"].tolist()]

        # then we embed them with fashion clip (batch size 32) and we normalize the embeddings
        image_embeddings = fclip.encode_images(images, 32)
        image_embeddings = image_embeddings / np.linalg.norm(image_embeddings, ord=2, axis=-1, keepdims=True)

        with open(EMBEDDING_PATH, "wb") as f:
            pickle.dump(image_embeddings, w)

    return image_embeddings


def search_image(**inputs):
    # loading the model (should be cached thanks to the loader)
    fclip = load_fclip()

    # loading the csv of the data
    subset = pd.read_csv("/workspace/cache_data/new_dataset/subset.csv")

    # loading the image embeddings
    image_embeddings = load_or_create_embeddings(fclip)

    # retrieving the query from the inputs
    query = inputs["query"]

    # create embeddings of the query (batch size 32 even if not necessary) and normalize it
    text_embedding = fclip.encode_text([query], 32)[0]
    text_embedding = text_embedding / np.linalg.norm(text_embedding)

    # dot product to find the matching object
    id_of_matched_object = np.argmax(text_embedding.dot(image_embeddings.T))
    found_object = subset["article_id"].iloc[id_of_matched_object].tolist()

    # finally we save the image
    image = Image.open("/workspace/cache_data/new_dataset/" + str(found_object) + ".jpg")

    image.save("output.png")
