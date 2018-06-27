class Config:

    def __init__(self):
        self.url_Project = ""
        self.email = ""
        self.password = ""
        self.stepWords = []

    def getUrlIssue(self):
        return self.url_Project
    
    def getEmail(self):
        return self.email
    
    def getPassword(self):
        return self.password
    
    def getStepWords(self):
        return self.stepWords