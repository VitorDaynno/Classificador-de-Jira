# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from jira_Api import Jira_Api
from classifier import Classifier

app = Flask("app")
jiras = open('jira.csv')

jira_api = Jira_Api()
classifier = Classifier()
items = []

for jira in jiras:
    aux = jira.split(',')
    item = {}
    item["key"] = aux[0]
    item["module"] = aux[2]
    item["moduleId"] = aux[3].replace("\r\n","")
    name = jira_api.getText(aux[0])
    item["name"] = name
    classifier.addVocabulary(name)
    items.append(item)    

jiras.close()

classifier.generateVocabularyBase()
classifier.removeStepWords()
classifier.createDatabaseTrainer(items)
classifier.createClassifier()

@app.route("/v1/classifiers",methods=["POST"])
def classifiers():
    body = request.json
    name = jira_api.getText(body["key"])
    response = classifier.predict(name)

    return jsonify({"module": response})

if __name__ == "__main__":
    app.run()
