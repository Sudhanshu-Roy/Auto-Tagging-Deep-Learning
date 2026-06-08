import re
import pickle
import numpy as np
import streamlit as st

from bs4 import BeautifulSoup

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load Tokenizer & Encoder

with open(r"models\tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open(r"models\mlb.pkl", "rb") as f:
    mlb = pickle.load(f)

# Parameters

MAX_LEN = 100
OPT_THRESHOLD = 0.25

VOCAB_SIZE = tokenizer.num_words + 1

# Recreate Architecture

model = Sequential([
    Embedding(
        input_dim=VOCAB_SIZE,
        output_dim=50,
        mask_zero=True
    ),

    SimpleRNN(
        128,
        activation="relu"
    ),

    Dense(
        128,
        activation="relu"
    ),

    Dense(
        10,
        activation="sigmoid"
    )
])

model.build((None, MAX_LEN))

# Load Weights

model.load_weights(
    r"models\weights_best.weights.h5"
)

print("Model Loaded Successfully")

# Text Cleaning

def cleaner(text):

    text = BeautifulSoup(
        text,
        "html.parser"
    ).get_text()

    text = re.sub(
        r"[^a-zA-Z]",
        " ",
        text
    )

    text = text.lower()

    tokens = text.split()

    return " ".join(tokens)

# Prediction

def predict_tags(text):

    cleaned_text = cleaner(text)

    seq = tokenizer.texts_to_sequences(
        [cleaned_text]
    )

    padded_seq = pad_sequences(
        seq,
        maxlen=MAX_LEN,
        padding="post"
    )

    pred_prob = model.predict(
        padded_seq,
        verbose=0
    )

    pred_binary = (
        pred_prob > OPT_THRESHOLD
    ).astype(int)

    predicted_tags = mlb.inverse_transform(
        pred_binary
    )

    if len(predicted_tags[0]) == 0:
        return ["No Tag Detected"]

    return list(predicted_tags[0])

# Streamlit UI

st.set_page_config(
    page_title="Auto Tag Generator",
    page_icon="🏷️"
)

st.title("🏷️ Auto Tag Generator")

st.write(
    "Enter a Stack Overflow style question and get predicted tags."
)

user_input = st.text_area(
    "Enter Question",
    height=200
)

if st.button("Predict Tags"):

    if not user_input.strip():

        st.warning(
            "Please enter some text."
        )

    else:

        tags = predict_tags(
            user_input
        )

        st.success(
            "Predicted Tags"
        )

        for tag in tags:
            st.markdown(
                f"- **{tag}**"
            )