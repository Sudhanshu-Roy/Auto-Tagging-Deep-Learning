# 🏷️ Auto Tag Generator using Deep Learning

A Deep Learning based NLP project that automatically predicts relevant Stack Overflow tags from user questions using Multi-Label Text Classification.

The project explores and compares multiple deep learning architectures including RNN, LSTM, GRU, and CNN, with CNN achieving the best performance and being selected for deployment.

---

## 🚀 Project Overview

Stack Overflow questions often require multiple tags to improve discoverability and categorization. Manually assigning tags can be time-consuming and inconsistent.

This project automates the tagging process by training deep learning models to predict multiple tags directly from question text.

---

## 🎯 Objectives

* Automatically generate relevant Stack Overflow tags
* Perform multi-label text classification
* Compare multiple deep learning architectures
* Deploy the best-performing model using Streamlit
* Build an end-to-end NLP pipeline from preprocessing to deployment

---

## 🧠 Models Evaluated

| Model | Macro F1 Score |
| ----- | -------------- |
| RNN   | 0.71           |
| LSTM  | 0.78           |
| GRU   | 0.82           |
| CNN   | 0.83           |

### Best Model

🏆 CNN achieved the highest Macro F1 Score of **0.83** and was selected for deployment.

---

## 📊 Dataset

Dataset consists of Stack Overflow questions and their associated tags.

Data Sources:

* Questions.csv
* Tags.csv

The dataset was transformed into a multi-label classification problem where each question can belong to multiple tags simultaneously.

---

## ⚙️ NLP Pipeline

### Text Preprocessing

* HTML Removal
* Text Cleaning
* Lowercase Conversion
* Tokenization
* Sequence Generation
* Sequence Padding
* Multi-Label Encoding

### Label Processing

* Tag Frequency Analysis
* Top Tag Selection
* MultiLabelBinarizer Encoding

---

## 🏗️ CNN Architecture

Embedding Layer
↓
Conv1D Layer (64 Filters)
↓
Dropout (0.1)
↓
GlobalMaxPooling1D
↓
Dense (128, ReLU)
↓
Dense (10, Sigmoid)

---

## 📈 Evaluation Metrics

The models were evaluated using:

* Precision
* Recall
* F1 Score
* Macro Average F1
* Classification Report

---

## 🖥️ Streamlit Application

The deployed application allows users to:

* Enter a Stack Overflow style question
* Predict relevant tags in real time
* View model-generated tag recommendations

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Libraries

* TensorFlow / Keras
* NumPy
* Pandas
* Scikit-Learn
* BeautifulSoup
* Streamlit

### NLP

* Text Cleaning
* Tokenization
* Multi-Label Classification

### Deployment

* Streamlit

---

## 📂 Project Structure

```text
Auto-Tagging-System/
│
├── app.py
├── requirements.txt
│
├── data/
│   ├── Questions.csv
│   └── Tags.csv
│
├── models/
│   ├── tokenizer.pkl
│   ├── mlb.pkl
│   │
│   ├── rnn/
│   ├── lstm/
│   ├── gru/
│   └── cnn/
│
├── notebooks/
│
├── screenshots/
│
└── README.md
```

---

## 💡 Key Learnings

* Multi-Label Text Classification
* Deep Learning for NLP
* Sequence Modeling
* CNNs for Text Classification
* Model Comparison & Selection
* Streamlit Deployment
* End-to-End Machine Learning Workflow

---

## 🔮 Future Improvements

* Transformer-based architectures (BERT)
* Attention Mechanisms
* Larger tag vocabulary
* Hyperparameter optimization
* Docker deployment
* Cloud deployment

---

## 👨‍💻 Author

Sudhanshu Roy

AI & Data Science Undergraduate

GitHub:
https://github.com/Sudhanshu-Roy
