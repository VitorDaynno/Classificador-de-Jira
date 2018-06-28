from configs.config import Config
import json
import requests
from requests.auth import HTTPBasicAuth

class Jira_Api:

    def __init__(self):
        print('Iniciando Jira_Api')
        self.config = Config()       

    def getText(self,key):    
        print('Iniciando busca em ' + key)    
        url = self.config.getUrlIssue().replace('{issueIdOrKey}',key)
        response = requests.get(url, auth=HTTPBasicAuth(self.config.getEmail(), self.config.getPassword()))
        jiras = json.loads(response.content)
       
        return jiras["fields"]["summary"] + " " + jiras["fields"]["description"]
