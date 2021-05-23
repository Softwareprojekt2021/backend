import mysql.connector
class DatabaseController:
    def __init__(self, config):
        self.host = config["DATABASE"]['host']
        self.port = config["DATABASE"]['port']
        self.user = config["DATABASE"]['user']
        self.password = config["DATABASE"]['password']
        self.database = config["DATABASE"]['database']
