from flask import Flask, request
import jwt
from mysql.connector import connect

import database.database as database
import configparser
import data.user
import data.offer

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config\\config.ini")
database_controller = database.DatabaseController(config)


@app.route("/login", methods=["POST"])
def login():
    json = request.get_json()
    if (verify_user(json["email"], json["password"])):
        user = database_controller.get_user_by_email(json["email"])
        return jwt.encode({"userId": user.get_id(), "admin": user.get_admin()}, config["TOKEN"]['secretkey'], algorithm="HS256"), 200
    else:
        return "", 404


@app.route("/universities", methods=["GET"])
def universities():
    universities = database_controller.get_all_universities()
    result = "["
    last = len(universities)-1
    for i, element in enumerate(universities):
        if(i != last):
            result += f'"{element.get_name()}",'
        else:
            result += f'"{element.get_name()}"'
    result += "]"
    return result, 200, {"Content-Type": "application/json"}


@app.route("/categories", methods=["GET"])
def categories():
    categories = database_controller.get_all_categories()
    result = "["
    last = len(categories)-1
    for i, element in enumerate(categories):
        if(i != last):
            result += f'"{element.get_name()}",'
        else:
            result += f'"{element.get_name()}"'
    result += "]"
    return result, 200, {"Content-Type": "application/json"}


@app.route("/users", methods=["GET"])
def users():
    users = database_controller.get_all_users()
    result = "["
    last = len(users)-1
    for i, element in enumerate(users):
        result += f"""{{"id":"{element.get_id()}","first_name":"{element.get_first_name()}","last_name":"{element.get_last_name()}"
,"e_mail":"{element.get_e_mail()}","course":"{element.get_course()}"
,"university":"{database_controller.get_university_by_id(element.get_university_id()).get_name()}","admin":"{str(element.get_admin()).lower()}" """
        picture = element.get_profile_picture()
        if (picture is not None):
            result += f""","profile_picture":"{picture}" """
        result += """}"""
        if(i != last):
            result += """,
"""
    result += "]"
    return result, 200, {"Content-Type": "application/json"}


@app.route("/user", methods=["GET"])
def user():
    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401
    user = database_controller.get_user_by_id(user_id)
    result = f"""{{"id":"{user.get_id()}","first_name":"{user.get_first_name()}","last_name":"{user.get_last_name()}"
,"e_mail":"{user.get_e_mail()}","course":"{user.get_course()}"
,"university":"{database_controller.get_university_by_id(user.get_university_id()).get_name()}","admin":"{str(user.get_admin()).lower()}" """
    picture = user.get_profile_picture()
    if (picture is not None):
        result += f""","profile_picture":"{picture}" """
    result += """}"""
    return result, 200, {"Content-Type": "application/json"}


@app.route("/user", methods=["DELETE"])
def delete_user():
    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401
    database_controller.delete_user(user_id)
    return "", 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    auth_header = request.headers["Authorization"]
    try:
        _, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401
    if (admin):
        if(database_controller.delete_user(user_id)):
            return "", 200
        else:
            return "", 404
    else:
        return "", 401


@app.route("/user", methods=["POST"])
def create_user():
    json = request.get_json()
    user = data.user.User(json["first_name"], json["last_name"], json["e_mail"], json["password"], json["course"],
                          database_controller.get_university_by_name(json["university"]).get_id())
    if("profile_picture" in json):
        user.set_profile_picture(json["profile_picture"])
    if (database_controller.create_user(user)):
        return "", 201
    else:
        return "", 409


@app.route("/user", methods=["PUT"])
def update_user():

    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401

    user = database_controller.get_user_by_id(user_id)
    json = request.get_json()
    if ("first_name" in json):
        user.set_first_name(json["first_name"])
    if ("last_name" in json):
        user.set_last_name(json["last_name"])
    if ("e_mail" in json):
        user.set_e_mail(json["e_mail"])
    if ("password" in json):
        user.set_password(json["password"])
    if ("course" in json):
        user.set_course(json["course"])
    if ("profile_picture" in json):
        user.set_profile_picture(json["profile_picture"])
    if ("university" in json):
        user.set_university_id(
            database_controller.get_university_by_name(json["university"]).get_id())
    if ("admin" in json and admin):
        user.set_admin(json["admin"])
    if (database_controller.update_user(user)):
        return "", 200
    else:
        return "", 409


@app.route("/offer/<offer_id>", methods=["GET"])
def get_offer(offer_id):
    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    offer = database_controller.get_offer_by_id(offer_id)
    if (offer is None):
        return "", 404
    result = f"""{{"id":"{offer.get_id()}","title":"{offer.get_title()}","compensation_type":"{offer.get_compensation_type()}"
    ,"price":"{offer.get_price()}","description":"{offer.get_description()}"
    ,"sold":{str(offer.get_sold()).lower()},"user_id":"{offer.get_user_id()}", "pictures":["""
    pictures = offer.get_pictures()
    last = len(pictures)-1
    for i, element in enumerate(pictures):
        if(i != last):
            result += f""" "{element}","""
        else:
            result += f""" "{element}" """

    result += """]}"""
    return result, 200, {"Content-Type": "application/json"}


@app.route("/offer/<offer_id>", methods=["DELETE"])
def delete_offer(offer_id):
    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    offer = database_controller.get_offer_by_id(offer_id)
    if(offer is None):
        return "", 404
    elif(offer.get_user_id() == user_id or admin):
        database_controller.delete_offer(offer_id)
        return "", 200
    else:
        return "", 401


@app.route("/offer", methods=["POST"])
def create_offer():

    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    json = request.get_json()
    offer = data.offer.Offer(json["title"], json["compensation_type"], json["price"],  json["description"],
                             json["sold"], database_controller.get_category_by_name(json["category"]).get_id(), user_id)
    if ("pictures" in json):
        for element in json["pictures"]:
            offer.add_picture(element)
    database_controller.create_offer(offer)
    return "", 200


# TODO picture update
@app.route("/offer", methods=["PUT"])
def update_offer():

    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    json = request.get_json()
    offer = database_controller.get_offer_by_id(json["id"])
    if(offer is None):
        return "", 404
    if(offer.get_user_id() != user_id):
        return "", 401
    if ("title" in json):
        offer.set_title(json["title"])
    if ("compensation_type" in json):
        offer.set_compensation_type(json["compensation_type"])
    if ("price" in json):
        offer.set_price(json["price"])
    if ("description" in json):
        offer.set_description(json["description"])
    if ("sold" in json):
        offer.set_sold(json["sold"])
    if ("category" in json):
        offer.set_category_id(
            database_controller.get_category_by_name(json["category"]).get_id())
    database_controller.update_offer(offer)
    return "", 200


@app.route("/offers", methods=["GET"])
def offers():

    auth_header = request.headers["Authorization"]
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    offer_ids = database_controller.get_offer_ids_by_user_id(user_id)
    if (offer_ids is None):
        return "", 404

    last_i = len(offer_ids)-1
    result = """["""
    for i, offer_id in enumerate(offer_ids):
        offer = database_controller.get_offer_by_id(offer_id)
        result += f"""{{"id":"{offer.get_id()}","title":"{offer.get_title()}","compensation_type":"{offer.get_compensation_type()}"
        ,"price":"{offer.get_price()}","description":"{offer.get_description()}"
        ,"sold":{str(offer.get_sold()).lower()},"user_id":"{offer.get_user_id()}", "pictures":["""
        pictures = offer.get_pictures()
        last_j = len(pictures)-1
        for j, element in enumerate(pictures):
            if(j != last_j):
                result += f""" "{element}","""
            else:
                result += f""" "{element}" """
        if(i != last_i):
            result += """]},
"""
        else:
            result += """]}"""

    result += """]"""
    return result, 200, {"Content-Type": "application/json"}


def verify_user(e_mail, password):
    user = database_controller.get_user_by_email(e_mail)
    if (user is not None):
        return user.get_password() == password
    else:
        return False


def decode_token(auth_header):
    token = jwt.decode(auth_header.split()[
                       1], config["TOKEN"]['secretkey'], algorithms="HS256")
    return token['userId'], token['admin']

# if __name__ == "__main__":
#    app.run(ssl_context=("cert\\cert.pem", "cert\\key.pem"))
