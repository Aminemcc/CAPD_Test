import os
import tensorflow as tf
import keras
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from flask import Flask, render_template, request

# template_folder = ""
# app = Flask(__name__, template_folder=template_folder)
# app.static_folder = 'static'

class CAPD_BOT:
    # DEEP LEARNING MODEL WITHOUT GPU NEEDED
    def __init__(self, model_name, tokenizer_name, data_name):
        self.template_folder = ""
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.static_folder = 'static'

        self.model = self.load_model(model_name)
        self.tokenizer = self.load_tokenizer(tokenizer_name)
        self.data = self.load_data(data_name)

        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()
        self.stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    
    def server(self):
        @self.app.route("/")        
        def home(self):
            return "Sahabat CAPD BOT API"
        
        @self.app.route("/getResponse")
        def getResponse(self):
            question = request.args.get('q')
            return self.ask(question)
        

    def clean(self, sentence):
        stemmed_sentence = self.stemmer.stem(sentence)
        filtered_sentence = self.stopword_remover.remove(stemmed_sentence)
        return filtered_sentence
    
    def load_model(self, model_name):
        return tf.keras.models.load_model(model_name)
    
    def load_tokenizer(self, tokenizer_name):
        with open(tokenizer_name, 'rb') as file:
            return pickle.load(file)
        
    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except:
            pass
        try:
            return pd.read_excel(filename)
        except:
            pass
        try:
            return pd.read_json(filename)
        except:
            return None
    
    def ask(self, question):
        q = self.clean(question)
        if not bool(q):
            return "Silahkan bertanya lagi", -1, 0
        sequences = self.tokenizer.texts_to_sequences([q])
        padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post', padding='post')
        prediction = self.model.predict(padded_sequences)
        predicted_label = np.argmax(prediction, axis=1)[0]
        predicted_ans = self.data[self.data['Label'] == predicted_label].iloc[0]["Answer"]
        confidence_score = prediction[0][predicted_label]
        return predicted_ans, predicted_label, confidence_score
    
    def run(self):
        self.server()
        self.app.run(host='0.0.0.0', port=8085)

    def runtest(self):
        question = ""
        while question != "exit":
            question = input(">> ")
            res, label, score = self.ask(question)
            print(res)
            print(score)
            print("-"*50)
    

model_name = "DL BiLSTM 10K.keras"
tokenizer_name = "tokenizer BiLSM 11183.pkl"
data_name = "FAQ_CAPD.xlsx"
bot = CAPD_BOT(model_name, tokenizer_name, data_name)
bot.run()
# bot.run()
# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route('/test')
# def getResponse2():
#     question = request.args.get('q')
#     if question:
#         res, _, _ = ask(question)
#         return res
#     else:
#         return "Silahkan bertanya."

# if __name__ == "__main__":
    
