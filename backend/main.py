import os
import re
import pickle
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from tensorflow.keras.layers import (
    Conv1D,
    Dense,
    Dropout,
    Embedding,
    GlobalMaxPooling1D,
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 100
OPT_THRESHOLD = 0.31
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]


def normalize_origin(value: str) -> str:
    return value.strip().rstrip("/")


def allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if not raw.strip():
        return DEFAULT_ORIGINS.copy()
    origins = [normalize_origin(origin) for origin in raw.split(",")]
    return [origin for origin in origins if origin]


ALLOWED_ORIGINS = allowed_origins()


def load_artifacts():
    with open(MODELS_DIR / "tokenizer.pkl", "rb") as handle:
        loaded_tokenizer = pickle.load(handle)

    with open(MODELS_DIR / "mlb.pkl", "rb") as handle:
        loaded_mlb = pickle.load(handle)

    vocab_size = loaded_tokenizer.num_words + 1
    loaded_model = Sequential(
        [
            Embedding(
                input_dim=vocab_size,
                output_dim=50,
                input_shape=(MAX_LEN,),
                mask_zero=True,
            ),
            Conv1D(filters=64, kernel_size=3, padding="same"),
            Dropout(0.1),
            GlobalMaxPooling1D(),
            Dense(128, activation="relu"),
            Dense(10, activation="sigmoid"),
        ]
    )
    loaded_model.build((None, MAX_LEN))
    loaded_model.load_weights(MODELS_DIR / "cnn" / "weights_best.weights.h5")
    return loaded_tokenizer, loaded_mlb, loaded_model


tokenizer, mlb, model = load_artifacts()

app = FastAPI(title="Auto Tag Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"],
    max_age=600,
)


class PredictRequest(BaseModel):
    text: str = Field(min_length=1, max_length=8000)

    @field_validator("text")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Please enter some text.")
        return value


class TagScore(BaseModel):
    name: str
    score: float


class PredictResponse(BaseModel):
    tags: list[TagScore]


def cleaner(text: str) -> str:
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower()
    return " ".join(text.split())


def predict_tags(text: str) -> list[TagScore]:
    cleaned_text = cleaner(text)
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN, padding="post")
    probabilities = model.predict(padded, verbose=0)[0]

    tags = [
        TagScore(name=str(label), score=round(float(probabilities[index]), 4))
        for index, label in enumerate(mlb.classes_)
        if probabilities[index] > OPT_THRESHOLD
    ]
    tags.sort(key=lambda tag: tag.score, reverse=True)
    return tags


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Please enter some text."
    errors = exc.errors()
    if errors:
        message = str(errors[0].get("msg", message))
        message = message.removeprefix("Value error, ")
    return JSONResponse(status_code=400, content={"detail": message})


@app.middleware("http")
async def restrict_predict_origin(request: Request, call_next):
    if request.url.path != "/api/predict":
        return await call_next(request)

    origin = normalize_origin(request.headers.get("origin", ""))
    if origin not in ALLOWED_ORIGINS:
        return JSONResponse(
            status_code=403,
            content={"detail": "This origin is not allowed to use the API."},
        )
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "service": "Auto Tag Generator",
        "health": "/health",
        "predict": "/api/predict",
    }


@app.post("/api/predict", response_model=PredictResponse)
def predict(body: PredictRequest):
    return PredictResponse(tags=predict_tags(body.text))
