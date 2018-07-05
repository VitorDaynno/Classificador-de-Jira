class Config:

    def __init__(self):
        self._url_project = ""
        self._email = ""
        self._password = ""
        self._step_words = []
        self._token_Yandex = ""
        self.read_step_words()

    def read_step_words(self):
        fileStepWords = open("configs/stepWords.txt", "r")
        self._stepWords = fileStepWords.read().split(";")
        fileStepWords.close()

    def get_url_issue(self):
        return self._url_project

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    def get_step_words(self):
        return self._stepWords

    def get_token_yandex(self):
        return self._token_Yandex
