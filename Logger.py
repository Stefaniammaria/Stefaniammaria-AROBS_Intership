from datetime import datetime

class Logger:
    def __init__(self):
        self.f = open("LogFile.txt","w")

    def log_message(self,message):
        now = datetime.now()
        self.f.write("[" + str(now) + "] " + message + "\n")

    def close_file(self):
        self.f.close()