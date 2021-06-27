import configparser
import datetime

from flask import Flask, request, json
from flask_cors import CORS
import jwt
from werkzeug.serving import WSGIRequestHandler

import database.database as database
import data.user
import data.offer
import data.rating
import data.watchlist_entry
import data.university
import data.message


# Fix for HTTP Connection closed while receiving Data
WSGIRequestHandler.protocol_version = "HTTP/1.1"
app = Flask(__name__)
CORS(app)

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
        return "", 204


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
        result += f"""{{"id":{element.get_id()},"first_name":"{element.get_first_name()}","last_name":"{element.get_last_name()}"
,"e_mail":"{element.get_e_mail()}","course":"{element.get_course()}"
,"university":"{database_controller.get_university_by_id(element.get_university_id()).get_name()}","admin":{str(element.get_admin()).lower()} """
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
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401
    user = database_controller.get_user_by_id(user_id)
    result = f"""{{"id":{user.get_id()},"first_name":"{user.get_first_name()}","last_name":"{user.get_last_name()}"
,"e_mail":"{user.get_e_mail()}","course":"{user.get_course()}"
,"university":"{database_controller.get_university_by_id(user.get_university_id()).get_name()}","admin":{str(user.get_admin()).lower()} """
    picture = user.get_profile_picture()
    if (picture is not None):
        result += f""","profile_picture":"{picture}" """
    result += """}"""
    return result, 200, {"Content-Type": "application/json"}


@app.route("/user", methods=["DELETE"])
def delete_user():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401
    database_controller.delete_user(user_id)
    return "", 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        _, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        return "", 401
    if (admin):
        if(database_controller.delete_user(user_id)):
            return "", 200
        else:
            return "", 204
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
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
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
    offer = database_controller.get_offer_by_id(offer_id)
    if (offer is None):
        return "", 204
    result = encode_offer(offer)
    return result, 200, {"Content-Type": "application/json"}


@app.route("/offer/<offer_id>", methods=["DELETE"])
def delete_offer(offer_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    offer = database_controller.get_offer_by_id(offer_id)
    if(offer is None):
        return "", 204
    elif(offer.get_user_id() == user_id or admin):
        database_controller.delete_offer(offer_id)
        return "", 200
    else:
        return "", 401


@app.route("/offer", methods=["POST"])
def create_offer():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
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


@app.route("/offer", methods=["PUT"])
def update_offer():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    json = request.get_json()
    offer = database_controller.get_offer_by_id(json["id"])
    if(offer is None):
        return "", 204
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
    if ("pictures" in json):
        offer.clear_picture()
        for pictures in json["pictures"]:
            offer.add_picture(pictures)
    database_controller.update_offer(offer)
    return "", 200


@app.route("/offers", methods=["GET"])
def offers():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    offer_ids = database_controller.get_offer_ids_by_user_id(user_id)
    if (len(offer_ids) == 0):
        return "", 204

    last_offer = len(offer_ids)-1
    result = """["""
    for i, offer_id in enumerate(offer_ids):
        offer = database_controller.get_offer_by_id(offer_id)
        result += encode_offer(offer)
        if(i != last_offer):
            result += """,
"""
    result += """]"""
    return result, 200, {"Content-Type": "application/json"}


@app.route("/offers/recommend", methods=["GET"])
def recommend_offers():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
        try:
            user_id, admin = decode_token(auth_header)
        except jwt.exceptions.InvalidTokenError:
            return "", 401
        user = database_controller.get_user_by_id(user_id)
        offer_ids = database_controller.get_recommend_offer_ids_by_user(user)
    else:
        offer_ids = database_controller.get_recommend_offer_ids_without_user()
    if (len(offer_ids) == 0):
        return "", 204

    last_offer = len(offer_ids)-1
    result = """["""
    for i, offer_id in enumerate(offer_ids):
        offer = database_controller.get_offer_by_id(offer_id)
        result += encode_offer(offer, True)
        if(i != last_offer):
            result += """,
"""
    result += """]"""
    return result, 200, {"Content-Type": "application/json"}


@app.route("/offers/filtered", methods=["GET"])
def filtered_offers():
    title = request.args.get("title", type=str)
    category = request.args.get("category", type=str)
    university = request.args.get("university", type=str)
    compensation_type = request.args.get("compensation_type", type=str)
    max_price = request.args.get("max_price", type=float)
    min_price = request.args.get("min_price", type=float)
    offer_ids = database_controller.get_filtered_offer_ids(
        title, category, university, compensation_type, max_price, min_price)
    if (len(offer_ids) == 0):
        return "", 204
    last_offer = len(offer_ids)-1
    result = """["""
    for i, offer_id in enumerate(offer_ids):
        offer = database_controller.get_offer_by_id(offer_id)
        result += encode_offer(offer, True)
        if(i != last_offer):
            result += """,
"""
    result += """]"""
    return result, 200, {"Content-Type": "application/json"}


@app.route("/watchlist/<offer_id>", methods=["POST"])
def add_watchlist_entry(offer_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    database_controller.add_watchlist_entry(
        data.watchlist_entry.Watchlist_entry(user_id, offer_id))
    return "", 200


@app.route("/watchlist/<offer_id>", methods=["DELETE"])
def delete_watchlist_entry(offer_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    database_controller.delete_watchlist_entry(
        data.watchlist_entry.Watchlist_entry(user_id, offer_id))
    return "", 200


@app.route("/watchlist", methods=["GET"])
def get_watchlist():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    watchlist = database_controller.get_watchlist(user_id)
    if (len(watchlist) == 0):
        return "",204
    last_element = len(watchlist)-1
    result = "["
    for i, element in enumerate(watchlist):
        result += encode_offer(database_controller.get_offer_by_id(
            element.get_offer_id()), True)
        if(i != last_element):
            result += f""",
"""
    result += "]"
    return result, 200


@app.route("/message/<offer_id>/create", methods=["POST"])
def create_chat(offer_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    chat_id = database_controller.create_chat(offer_id, user_id)
    return f"""{{"chat_id":{chat_id}}}""", 200


@app.route("/message/<chat_id>", methods=["POST"])
def add_message(chat_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    if(not database_controller.is_chat_of_user(chat_id, user_id)):
        return "", 401
    json = request.get_json()
    text = json["text"]
    timestamp = datetime.datetime.now()
    database_controller.add_message(data.message.Message(
        user_id, chat_id, text, timestamp))
    return "", 200


@app.route("/message/<chat_id>", methods=["GET"])
def get_conversation(chat_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    if(not (database_controller.is_chat_of_user(chat_id, user_id) or admin)):
        return "", 401
    conversation = database_controller.get_conversation(chat_id)
    last_element = len(conversation)-1
    result = "["
    for i, element in enumerate(conversation):
        result += f"""{{"message_id":{element.get_id()},"user_id":{element.get_user_id()},"text":"{element.get_text()}","timestamp":"{element.get_timestamp()}"}}"""
        if(i != last_element):
            result += f""","""
    result += "]"
    return result, 200


@app.route("/message/<chat_id>/<message_id>", methods=["DELETE"])
def delete_message(chat_id, message_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    if (database_controller.is_message_of_user(message_id, chat_id, user_id) or admin):
        database_controller.delete_message(chat_id, message_id)
        return "", 200
    else:
        return "", 401


@app.route("/messages", methods=["GET"])
def get_conversations():
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401

    conversations = database_controller.get_conversations(user_id)
    if (len(conversations) == 0):
        return "",204
    last_element = len(conversations)-1
    result = "["
    for i, element in enumerate(conversations):
        result += f"""{element}"""
        if(i != last_element):
            result += f""","""
    result += "]"
    return result, 200


@app.route("/messages/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    if (database_controller.is_chat_of_user(chat_id, user_id) or admin):
        database_controller.delete_chat(chat_id)
        return "", 200
    else:
        return "", 401


@app.route("/rating/<user_id>", methods=["POST"])
def create_rating(user_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        login_user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    if(login_user_id == int(user_id)):
        return "", 401
    json = request.get_json()
    database_controller.create_rating(
        data.rating.Rating(json["rating"], login_user_id, user_id))
    return "", 200


@app.route("/rating/<user_id>", methods=["PUT"])
def update_rating(user_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        login_user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    json = request.get_json()
    database_controller.update_rating(
        data.rating.Rating(json["rating"], login_user_id, user_id))
    return "", 200


@app.route("/rating/<user_id>", methods=["GET"])
def get_rating(user_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        login_user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    average_rating = database_controller.get_average_rating(user_id)
    return f"""{{"average_rating":{average_rating}}}""", 200


@app.route("/rating/<user_id>", methods=["DELETE"])
def delete_rating(user_id):
    if ("Authorization" in request.headers):
        auth_header = request.headers["Authorization"]
    else:
        return "", 401
    try:
        login_user_id, admin = decode_token(auth_header)
    except jwt.exceptions.InvalidTokenError:
        return "", 401
    database_controller.delete_rating(login_user_id, user_id)
    return "", 200


def verify_user(e_mail, password):
    user = database_controller.get_user_by_email(e_mail)
    if (user is not None):
        return user.get_password() == password
    else:
        return False


def decode_token(auth_header):
    token = jwt.decode(auth_header.split()[1],
                       config["TOKEN"]['secretkey'], algorithms="HS256")
    return token['userId'], token['admin']


def encode_offer(offer, one_image=False):
    user = database_controller.get_user_by_id(offer.get_user_id())
    result = f"""{{"id":{offer.get_id()},"title":"{offer.get_title()}","compensation_type":"{offer.get_compensation_type()}"
,"price":"{offer.get_price()}","description":{json.dumps(offer.get_description())},"category":"{database_controller.get_category_by_id(offer.get_category_id()).get_name()}"
,"sold":{str(offer.get_sold()).lower()}
,"user":{{"first_name":"{user.get_first_name()}","last_name":"{user.get_last_name()}","e_mail":"{user.get_e_mail()}"
,"average_rating":{database_controller.get_average_rating(offer.get_user_id())}}}, "pictures":["""
    pictures = offer.get_pictures()
    if (not one_image):
        last_picture = len(pictures)-1
        for i, element in enumerate(pictures):
            result += f""" "{element}" """
            if(i != last_picture):
                result += f""","""
    elif(len(pictures) > 0):
        result += f""" "{pictures[0]}" """
    result += """]}"""
    return result

# if __name__ == "__main__":
#    app.run(ssl_context=("cert\\cert.pem", "cert\\key.pem"))
