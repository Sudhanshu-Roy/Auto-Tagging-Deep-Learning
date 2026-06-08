# Automatic Tag Generator using RNN

## Overview

This project automatically predicts relevant tags for Stack Overflow style questions using Natural Language Processing (NLP) and Recurrent Neural Networks (RNNs).

The model is trained on Stack Overflow questions and their associated tags, enabling automatic multi-label tag prediction for unseen text.

---

## Features

* Text preprocessing and cleaning
* Multi-label classification
* RNN-based deep learning model
* Real-time prediction using Streamlit
* Automatic tag generation

---

## Tech Stack

* Python
* TensorFlow / Keras
* Streamlit
* Scikit-Learn
* Pandas
* NumPy
* BeautifulSoup

---

## Project Structure

```text
Auto-Tagging-RNN/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── weights_best.weights.h5
│   ├── tokenizer.pkl
│   └── mlb.pkl
│
├── notebooks/
│   └── Auto_Tagging_RNN.ipynb
│
└── screenshots/
```

---

## Installation

```bash
git clone <repository-url>

cd Auto-Tagging-RNN

pip install -r requirements.txt

streamlit run app.py
```

---

## Example

Input:

```text
How can I fit a logistic regression model using scikit-learn?
```

Predicted Tags:

```text
machine learning
scikit learn
classification
```

---

## Future Improvements

* LSTM-based architecture
* BiLSTM implementation
* Attention Mechanism
* Transformer-based models (BERT)
* Deployment to cloud platforms

---

## Author

Sudhanshu Roy
