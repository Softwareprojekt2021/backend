import mysql.connector
import database.database
import configparser

filename = "res\\sql\\Create.sql"
try:
    querry = open(filename, "r").read()
except OSError:
    print("Die Datei {filename} konnte nicht geöffnet werden.")

config = configparser.ConfigParser()
config.read("config\\config.ini")

connection = mysql.connector.connect(
    host=config["DATABASE"]['host'], port=config["DATABASE"]['port'], user="Admin", password="j,#{TK:Z,uc78mPX")
cursor = connection.cursor()
cursor.execute(querry, multi=True)
cursor.fetchall()
cursor.close()
connection.close()
