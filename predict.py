from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
import string
import re
from lib_file import lib_path


model = load_model(filepath="model/ConvolutionalLongShortTermMemory_model.h5")

with open(file="model/tokens.pkl", mode="rb") as file:
    tok = pickle.load(file=file)

class_names = {0: 'Cyberbullying', 1: 'Not-Cyberbullying'}

nlp = spacy.load("en_core_web_sm")
print(nlp.pipe_names)

punctuations = string.punctuation

cList = pickle.load(open('model/cword_dict.pkl', 'rb'))
c_re = re.compile('(%s)' % '|'.join(cList.keys()))


def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group()]
    return c_re.sub(replace, text)


def preprocess_text(docx):
    sentence = [word.lemma_.lower().strip() if word.lemma_ !=
                "-PRON-" else word.lower_ for word in docx]
    sentence = [
        word for word in sentence if word not in stopwords and word not in punctuations]
    sentence = [word for word in sentence if len(word) > 1 and word.isalpha()]
    return sentence


def model_prediction(text_file):
    # Expand contractions
    expanded_text = expandContractions(str(text_file))

    # Preprocess the text
    sp_sentes = nlp(text=expanded_text)
    cleaned = preprocess_text(sp_sentes)

    # Tokenize and pad the text
    num_data = tok.texts_to_sequences([cleaned])
    pad_text = pad_sequences(sequences=num_data, maxlen=50, padding="post")

    # Predict using the model
    model_prediction = model.predict(pad_text)
    prediction_value = model_prediction[0][0]  # Take the 0 index value
    if prediction_value >= 0.30:  # Threshold to classify
        prediction = 'Cyberbullying'
    else:
        prediction = 'Not-Cyberbullying'

    return prediction
