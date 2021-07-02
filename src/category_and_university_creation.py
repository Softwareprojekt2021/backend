import configparser
import mysql.connector

filename_category = "res\\category.txt"
filename_university = "res\\university.txt"
try:
    file_category = open(filename_category, "r", encoding="utf-8")
    category = [line.strip() for line in file_category.readlines() if len(line.strip()) > 0]
    file_category.close()
    file_university = open(filename_university, "r", encoding="utf-8")
    university = [line.strip() for line in file_university.readlines() if len(line.strip()) > 0]
    file_university.close()
except OSError:
    print("Die Datei {filename} konnte nicht geöffnet werden.")

querry_category = """INSERT INTO category (title) VALUES """
last_element = len(category)-1
for i, element in enumerate(category):
    querry_category += f""" ("{element}") """
    if(i != last_element):
        querry_category += f""","""

querry_university = """INSERT INTO university (university) VALUES """
last_element = len(university)-1
for i, element in enumerate(university):
    querry_university += f""" ("{element}") """
    if(i != last_element):
        querry_university += f""","""

config = configparser.ConfigParser()
config.read("config\\config.ini")

connection = mysql.connector.connect(
    host=config["DATABASE"]['host'], port=config["DATABASE"]['port'], user=config["DATABASE"]['user'], password=config["DATABASE"]['password'],database = config["DATABASE"]['database'])

cursor = connection.cursor()
cursor.execute(querry_category)
cursor.execute(querry_university)
connection.commit()
cursor.fetchall()
cursor.close()
connection.close()