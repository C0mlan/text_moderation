from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from datetime import timedelta
from .models import MyAPIKey
import joblib
import os
import re
import string
from nltk.corpus import stopwords
import __main__
import logging

logging.getLogger('absl').setLevel(logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

#this reset the usage_count
def reset_keylimit():
    current_time = now()
    keys = MyAPIKey.objects.all()

    for key in keys:
        if key.last_reset is None or (current_time - key.last_reset) >= timedelta(minutes=9):
            key.usage_count = 0
            key.last_reset = current_time
            key.save()
            print(f"[{current_time}] Usage reset triggered for {key.user.username}")

#starts the ApSchedular
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_keylimit, 'cron', minute ='*/10')
    scheduler.start()



stop_words = set(stopwords.words('english'))




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))





TOXIC_MODEL_PATH = os.path.join(BASE_DIR, 'train_model/toxic_model.h5')
TOXIC_TOKENIZER = os.path.join(BASE_DIR, "train_model/tokenizer.pkl")
SPAM_MODEL_PATH = os.path.join(BASE_DIR, 'train_model/spam_pipeline.pkl')


#SPAM_PREDICT
def process_text(text):
    
    nopunc = "".join(char for char in text if char not in string.punctuation)

    clean_words = [word for word in nopunc.split() if word.lower() not in stop_words]
    
    return clean_words

__main__.process_text = process_text


spam_model = joblib.load(SPAM_MODEL_PATH)

def predict_spam(text, model=spam_model):
    if not text:
        return "Text is required."

    prediction = model.predict([text])[0]
    return "SPAM" if prediction == 1 else "HAM"

# TOXIC_PREDICT
model = load_model(TOXIC_MODEL_PATH)
with open(TOXIC_TOKENIZER, "rb") as f:
    tokenizer = joblib.load(f)

MAX_SEQUENCE_LENGTH = 200

def clean_text(text, remove_stopwords=True):
    output = ""
    text = str(text).replace('\n', ' ')
    text = re.sub(r'[^\w\s]', '', text).lower()
    if remove_stopwords:
        text = text.split(" ")
        for word in text:
            if word not in stopwords.words('english'):
                output += ' ' + word
    else:
        output = text
    return output.strip()

def predict_comment(comment):
    cleaned = clean_text(comment)
    sequence = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH)
    pred = model.predict(padded, verbose=0)[0]

    labels = ["identity_hate", "insult", "threat", "obscene"]
    result = {label: float(prob) for label, prob in zip(labels, pred)}
    binary = {label: int(prob > 0.4) for label, prob in result.items()}
    return {"probabilities": result, "prediction": binary}

