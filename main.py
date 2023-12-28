from src.utils import *

@app.get("/")
@app.get("/{name}")
def index(name: str = "There"):
    response = f"Hey {name}!"
    return response


@app.get("/sentiment/{text}")
def sentiment_route(text: str):
    clean_text = text_cleaner(text)[0]
    return {"sentiment": model.predict_sentiment(clean_text)}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
