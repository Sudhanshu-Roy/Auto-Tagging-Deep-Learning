import re
import pickle
import streamlit as st

from bs4 import BeautifulSoup

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Embedding,
    Conv1D,
    Dropout,
    GlobalMaxPooling1D,
    Dense
)

from tensorflow.keras.preprocessing.sequence import pad_sequences

# Configuration

MAX_LEN = 100
OPT_THRESHOLD = 0.31


# -----------------------------
# Load Tokenizer & Encoder
# -----------------------------

with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("models/mlb.pkl", "rb") as f:
    mlb = pickle.load(f)


VOCAB_SIZE = tokenizer.num_words + 1

# CNN Model Architecture

model = Sequential([
    Embedding(
        input_dim=VOCAB_SIZE,
        output_dim=50,
        input_shape=(MAX_LEN,),
        mask_zero=True
    ),

    Conv1D(
        filters=64,
        kernel_size=3,
        padding="same"
    ),

    Dropout(0.1),

    GlobalMaxPooling1D(),

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

model.load_weights(
    "models/cnn/weights_best.weights.h5"
)

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

    return " ".join(
        text.split()
    )

# Prediction Function

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
    page_icon="🏷️",
    layout="centered"
)

st.title("🏷️ Auto Tag Generator")

st.markdown(
    """
    Predict Stack Overflow tags using a **CNN-based
    Multi-Label NLP Classification Model**.

    **Model Performance**
    - Macro F1 Score: **0.83**
    - Architecture: **CNN**
    """
)

user_input = st.text_area(
    "Enter Question",
    height=200,
    placeholder="Type your Stack Overflow question here..."
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

        cols = st.columns(
            min(len(tags), 4)
        )

        for i, tag in enumerate(tags):

            cols[i % 4].metric(
                "Tag",
                tag
            )