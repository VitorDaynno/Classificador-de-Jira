#-*- coding: utf-8 -*-
from yandex_translate import YandexTranslate
import numpy as np
from sklearn import linear_model
from configs.config import Config

class Classifier:

    def __init__(self):
        print('Iniciando Classifier')
        self.vocabulary = []
        self.modules = {}
        self.input_vector = []
        self.output_vector = []
        self.config = Config()
        self.translator = YandexTranslate(self.config.get_token_yandex()) 

    def add_vocabulary(self, phrase):
        phrase = self.translator.translate(phrase, 'pt-en')['text'][0]
        words = phrase.split(' ')
        for word in words:
            if self._format_word(word) not in self.vocabulary:
                self.vocabulary.append(self._format_word(word))

    def _format_word(self, word):
        word = word.lower()
        word = word.replace('"','')
        word = word.replace("'","")
        word = word.replace("(","")
        word = word.replace(")","")
        #word = word.encode('utf-8')
        word = word.replace("\n","")
        word = word.replace("\r","")
        word = word.replace(".","")
        word = word.replace("!","")
        word = word.replace(":","")
        word = word.replace("-","")
        word = word.replace(",","")
        word = word.replace("<","")
        word = word.replace(">","")
        word = word.replace("[","")
        word = word.replace("]","")
        word = word.replace("?","")
        word = word.replace("+","")
        word = word.replace("”","")
        word = word.replace(";","")
        word = word.replace("*","")
        word = word.replace("~","")
        word = word.replace("_","")
        word = word.replace("¿","")      
        word = word.replace("^","")
        word = word.replace("’","")              
        print(word)
        return word
    
    def remove_step_words(self):
        step_words = self.config.get_step_words()
        for step_word in step_words:
            if(step_word in self.vocabulary):
                self.vocabulary.remove(step_word)

    def create_database_trainer(self, items):
        for item in items:
            i = 0
            vector = []
            self.modules[item["moduleId"]] = item["module"]
            while i < len(self.vocabulary):
                if self.vocabulary[i] in item["name"].split(" "):
                    vector.append(1)
                else:
                    vector.append(0)
                i = i + 1
            self.input_vector.append(vector)
            self.output_vector.append(item["moduleId"])
    
    def create_classifier(self):
        input_vector = np.array(self.input_vector)
        output_vector = np.array(self.output_vector)

        self.model = linear_model.LinearRegression().fit(input_vector, output_vector)

    def predict(self, name):
        name = self.translator.translate(name, 'pt-en')['text'][0]
        vector = self.vectorize(name)
        print(self.model.predict(np.array([ vector ])))
        index = round(self.model.predict(np.array([ vector ]))[0],0)
        print(index)
        if str(int(index)) in self.modules:
            return self.modules[str(int(index))]
        else:
            return "Modulo não encontrado"


    def vectorize(self,phrase):
        i = 0
        vector = []
        while i < len(self.vocabulary):
            if self.vocabulary[i] in phrase.split(" "):
                vector.append(1)
            else:
                vector.append(0)
            i = i + 1
        return vector

    def generate_vocabulary_base(self):
        vocabulary_base = open("configs/vocabularyBase.txt","w")       
        for word in self.vocabulary:
            vocabulary_base.write(word + "\n")
        vocabulary_base.close()
