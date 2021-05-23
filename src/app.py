from flask import Flask, request
import jwt

import database.database as database
import configparser
import data.user
import data.offer

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config\\config.ini")
databaseController = database.DatabaseController(config)


@app.route("/login", methods=["POST"])
def login():
    json = request.get_json()
    if (verify_user(json["email"], json["password"])):
        return "", 200
    else:
        return "", 404


@app.route("/universities", methods=["GET"])
def universities():
    universities = databaseController.get_all_universities()
    result = "["
    last = len(universities)-1
    for i, element in enumerate(universities):
        if(i != last):
            result += f'"{element.get_name()}",'
        else:
            result += f'"{element.get_name()}"'
    result += "]"
    return result, 200, {"Content-Type": "application/json"}


# TODO test
@app.route("/users", methods=["GET"])
def users():
    users = databaseController.get_all_users()
    result = "["
    last = len(users)-1
    for i, element in enumerate(users):
        if(i != last):
            result += f"""{{"id":"{element.get_id()}","first_name":"{element.get_first_name()}","last_name":"{element.get_last_name()}"
    ,"e_mail":"{element.get_e_mail()}","password":"{element.get_password()}"
    ,"course":"{element.get_course()}","profile_picture":"{element.get_profile_picture_base64()}"
    ,"university":"{databaseController.get_university_by_id(element.get_university_id()).get_name()}","admin":"{element.get_admin()}"}},"""
        else:
            result += f"""{{"id":"{element.get_id()}","first_name":"{element.get_first_name()}","last_name":"{element.get_last_name()}"
    ,"e_mail":"{element.get_e_mail()}","password":"{element.get_password()}"
    ,"course":"{element.get_course()}","profile_picture":"{element.get_profile_picture_base64()}"
    ,"university":"{databaseController.get_university_by_id(element.get_university_id()).get_name()}","admin":"{element.get_admin()}"}}"""
    result += "]"
    return result, 200, {"Content-Type": "application/json"}


@app.route("/user", methods=["POST"])
def create_user():
    json = request.get_json()
    user = data.user.User(json["first_name"], json["last_name"], json["e_mail"], json["password"], json["course"],
                          databaseController.get_university_by_name(json["university"]).get_id(), json["admin"])
    user.set_profile_picture_base64(json["profile_picture"])
    if (databaseController.create_user(user)):
        return "", 201
    else:
        return "", 409


# TODO SESSION MANEGMENT
@app.route("/user", methods=["PUT"])
def update_user():
    json = request.get_json()
    user = databaseController.get_user_by_id(int(json["id"]))
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
        user.set_profile_picture_base64(json["profile_picture"])
    if ("university" in json):
        user.set_university_id(
            databaseController.get_university_by_name(json["university"]).get_id())
    if ("admin" in json):
        user.set_admin(json["admin"])
    databaseController.update_user(user)
    return "", 200


# TODO test
@app.route("/offer/<offerid>", methods=["GET"])
def get_offer(offerid):
    offer = databaseController.get_offer_by_id(int(offerid))
    return f"""{{"id":"{offer.get_id()}","title":"{offer.get_title()}","compensation_type":"{offer.get_compensation_type()}"
    ,"price":"{offer.get_price()}","description":"{offer.get_description()}"
    ,"sold":"{offer.get_sold()}","user_id":"{offer.get_user_id()}"}}""", 200, {"Content-Type": "application/json"}


# TODO test
# # TODO SESSION MANEGMENT
@app.route("/offer/<offerid>", methods=["DELETE"])
def delete_offer(offerid):
    databaseController.delete_offer(int(offerid))
    return "", 200


# TODO test
# TODO SESSION MANEGMENT
@app.route("/offer", methods=["POST"])
def create_offer():
    json = request.get_json()
    offer = data.offer.Offer(json["title"], json["compensation_type"], json["price"],  json["description"],
                             json["sold"], databaseController.get_category_by_name(json["category"]).get_id, json["user_id"])
    databaseController.create_offer(offer)
    return "", 200


# TODO test
# TODO SESSION MANEGMENT
@app.route("/offer", methods=["PUT"])
def update_offer():
    json = request.get_json()
    offer = databaseController.get_offer_by_id(int(json["id"]))
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
        offer.set_category(json["category"])
    if ("user_id" in json):
        offer.set_user_id(json["user_id"])
    databaseController.update_offer(offer)
    return "", 200


def verify_user(e_mail, password):
    user = databaseController.get_user_by_email(e_mail)
    return user.get_password() == password

# if __name__ == "__main__":
#    app.run(ssl_context=("cert\\cert.pem", "cert\\key.pem"))
