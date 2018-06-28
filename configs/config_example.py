class Config:

    def __init__(self):
        self._url_Project = ""
        self._email = ""
        self._password = ""
        self._stepWords = []
        self.read_step_words()

    def read_step_words(self):
        fileStepWords = open("configs/stepWords.txt", "r")
        self._stepWords = fileStepWords.read().split(";")
        fileStepWords.close()

    def getUrlIssue(self):
        return self._url_Project
    
    def getEmail(self):
        return self._email
    
    def getPassword(self):
        return self._password
    
    def getStepWords(self):
        return self._stepWords