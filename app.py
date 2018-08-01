# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from jira_Api import Jira_Api
from classifier import Classifier
from mongo_DAO import Mongo_DAO

app = Flask("app")
jiras = open('jira.csv')

jira_api = Jira_Api()
classifier = Classifier()
dao = Mongo_DAO('localhost', 27017, 'classifier')
items = []

for jira in jiras:
    aux = jira.split(',')
    item = {}
    item["key"] = aux[0]
    item["module"] = aux[1]
    item["moduleId"] = aux[2].replace("\n","")
    name = jira_api.get_text(aux[0])
    item["text"] = name
    dao.insert('jiras', item)
    item['textEn'] = classifier.add_vocabulary(item['key'], name)    
    items.append(item)    

jiras.close()

classifier.generate_vocabulary_base()
classifier.remove_step_words()
classifier.create_database_trainer(items)
classifier.create_classifier()

@app.route("/v1/classifiers",methods=["POST"])
def classifiers():
    body = request.json
    name = jira_api.get_text(body["key"])
    response = classifier.predict(name)

    return jsonify({"module": response})

if __name__ == "__main__":
    app.run()
