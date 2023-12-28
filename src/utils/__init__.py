from fastapi import FastAPI
from src.models.sentiments import Sentiment
from src.cleaners.text_cleaner import TextCleaner

import os
import uvicorn
import warnings

warnings.filterwarnings("ignore")

DATA_DIR = "src/models"
MODEL_PATH = f"{DATA_DIR}/model"
model = Sentiment(MODEL_PATH)

cleaner = TextCleaner()
text_cleaner = (
    lambda text: cleaner.clean_sentences([text])[0]
    if cleaner.clean_sentences([text])[0]
    else ["neutral"]
)

app = FastAPI()

DATA_DIR = "src/models"
HOST = "0.0.0.0"
PORT = 5000
