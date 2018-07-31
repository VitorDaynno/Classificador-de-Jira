from requests.auth import HTTPBasicAuth
import requests
import json
from configs.config import Config

class Jira_Api:

    def __init__(self):
        print('Iniciando Jira_Api')
        self.config = Config()       

    def get_text(self,key):    
        print('Iniciando busca em ' + key)    
        url = self.config.get_url_issue().replace('{issueIdOrKey}',key)
        response = requests.get(url, auth=HTTPBasicAuth(self.config.get_email(), self.config.get_password()))
        jiras = response.json()

        description = jiras["fields"]["description"] if jiras["fields"]["description"] != None else ""
        return jiras["fields"]["summary"] + " " + description
