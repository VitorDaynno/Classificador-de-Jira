#-*- coding: utf-8 -*-
from yandex_translate import YandexTranslate
from configs.config import Config
import numpy as np
from sklearn import linear_model

class Classifier:

    def __init__(self):
        print('Iniciando Classifier')
        self.vocabulary = []
        self.modules = {}
        self.input_vector = []
        self.output_vector = []
        self.config = Config()
        self.translator = YandexTranslate(self.config.get_token_yandex()) 

    def addVocabulary(self, phrase):
        phrase = self.translator.translate(phrase, 'pt-en')['text'][0]
        words = phrase.split(' ')
        for word in words:
            if self.formatWord(word) not in self.vocabulary:
                self.vocabulary.append(self.formatWord(word))

    def formatWord(self, word):
        word = word.lower()
        word = word.replace('"','')
        word = word.replace("'","")
        word = word.replace("(","")
        word = word.replace(")","")
        word = word.encode('utf-8')
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
                
        return word
    
    def removeStepWords(self):
        stepWords = self.config.getStepWords()
        for stepWord in stepWords:
            if(stepWord in self.vocabulary):
                self.vocabulary.remove(stepWord)

    def createDatabaseTrainer(self, items):
        for item in items:
            i = 0
            vector = []
            self.modules[item["moduleId"]] = item["module"]
            while i < len(self.vocabulary):
                if self.vocabulary[i] in item["name"].encode("utf-8").split(" "):
                    vector.append(1)
                else:
                    vector.append(0)
                i = i + 1
            self.input_vector.append(vector)
            self.output_vector.append(item["moduleId"])
    
    def createClassifier(self):
        input_vector = np.array(self.input_vector)
        output_vector = np.array(self.output_vector)

        self.model = linear_model.LinearRegression().fit(input_vector, output_vector)

    def predict(self, name):
        name = self.translator.translate(name, 'pt-en')['text'][0]
        vector = self.vectorize(name)
        index = round(self.model.predict(np.array([ vector ])),0)
        if str(int(index)) in self.modules:
            return self.modules[str(int(index))]
        else:
            return "Modulo não encontrado"


    def vectorize(self,phrase):
        i = 0
        vector = []
        while i < len(self.vocabulary):
            if self.vocabulary[i] in phrase.encode("utf-8").split(" "):
                vector.append(1)
            else:
                vector.append(0)
            i = i + 1
        return vector

    def generateVocabularyBase(self):
        vocabularyBase = open("configs/vocabularyBase.txt","w")       
        for word in self.vocabulary:
            vocabularyBase.write(word + "\n")
        vocabularyBase.close()
