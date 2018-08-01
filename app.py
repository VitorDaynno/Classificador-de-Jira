# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from jira_Api import Jira_Api
from classifier import Classifier
from mongo_DAO import Mongo_DAO

ind = 1

app = Flask("app")
classifier = Classifier()
jira_api = Jira_Api()
dao = Mongo_DAO('localhost', 27017, 'classifier')
items = []

if ind == 1:
    jiras = dao.find('jiras',{})
    
    for jira in jiras:
        print(jira['key'])
        item = jira
        #item['textEn'] = classifier.add_vocabulary(item['key'], item['text'])    
        items.append(item)
    
    vocabulary = dao.find('base',{})
    classifier.set_vocabulary(vocabulary[0]['words'])

elif ind == 0:
    jiras = open('jira.csv')
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
