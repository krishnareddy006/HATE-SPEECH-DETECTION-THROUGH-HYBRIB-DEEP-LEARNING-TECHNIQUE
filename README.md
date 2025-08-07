# 🧠 Hate Speech Detection through Hybrid Deep Learning Technique

A robust and scalable web application that leverages hybrid deep learning techniques to detect hate speech in textual data. This project combines NLP preprocessing, LSTM-based deep learning, and Flask deployment to provide real-time predictions through a user-friendly interface.

---

## 🚀 Features

- ✅ Real-time hate speech detection from user input
- 🔄 Advanced text preprocessing (cleaning, stopword removal, lemmatization)
- 🔤 Tokenization and sequence padding
- 🤖 Hybrid LSTM-based model trained on labeled data
- 🌐 Web interface using Flask
- 📦 Model persistence using Pickle

---

## 🧰 Tech Stack

| Category      | Tools Used                   |
|---------------|------------------------------|
| Language      | Python                       |
| Deep Learning | TensorFlow, Keras (LSTM)     |
| NLP           | NLTK, re (regex), Pandas     |
| Web Framework | Flask                        |
| Model Storage | Pickle                       |
| Deployment    | Localhost via Flask          |

---

## 🧪 Model Information

- **Type**: LSTM (Long Short-Term Memory)
- **Input**: Cleaned and tokenized text
- **Output**: Binary label – Hate Speech or Not
- **Dataset**: Preprocessed labeled text data (not included in repo)
- **Training**: Conducted in Jupyter Notebook (`hate_speech_detection.ipynb`)

---

## 🔍 How It Works

1. User inputs a text string via web UI
2. The text is preprocessed (cleaning, lemmatizing, stopword removal)
3. The sequence is tokenized and padded
4. The loaded model (`final_model.pkl`) makes a prediction
5. Result is displayed: "Hate Speech" or "Not Hate Speech"

---

