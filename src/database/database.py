import mysql.connector

import data.user
import data.university
import data.category
import data.offer
import data.rating
import data.watchlist_entry
import data.chat


class DatabaseController:
    def __init__(self, config):
        self.host = config["DATABASE"]['host']
        self.port = config["DATABASE"]['port']
        self.user = config["DATABASE"]['user']
        self.password = config["DATABASE"]['password']
        self.database = config["DATABASE"]['database']

    def get_user_by_email(self, e_mail):
        query = "SELECT first_name,last_name,e_mail,password,course,TO_BASE64(profile_picture),university_id,admin,id FROM user WHERE e_mail = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (e_mail,))
        result = cursor.fetchone()
        if (result is not None):
            first_name, last_name, e_mail, password, course, profile_picture, university_id, admin, id = result
            if(admin == 1):
                admin = True
            elif(admin == 0):
                admin = False
            user = data.user.User(
                first_name, last_name, e_mail, password, course, university_id, admin, id)
            user.set_profile_picture(profile_picture)
        else:
            user = None
        cursor.close()
        connection.close()
        return user

    def get_user_by_id(self, id):
        query = "SELECT first_name,last_name,e_mail,password,course,TO_BASE64(profile_picture),university_id,admin,id FROM user WHERE id = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if (result is not None):
            first_name, last_name, e_mail, password, course, profile_picture, university_id, admin, id = result
            if(admin == 1):
                admin = True
            elif(admin == 0):
                admin = False
            user = data.user.User(
                first_name, last_name, e_mail, password, course, university_id, admin, id)
            user.set_profile_picture(profile_picture)
        else:
            user = None
        cursor.close()
        connection.close()
        return user

    def create_user(self, user):
        if (self.get_user_by_email(user.get_e_mail()) is not None):
            return False
        query = """INSERT INTO 
        user (first_name,last_name,e_mail,password,course,profile_picture,admin,university_id) 
        VALUES (%s,%s,%s,%s,%s,FROM_BASE64(%s),%s,%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        if (user.get_admin()):
            admin = 1
        else:
            admin = 0
        cursor.execute(query, (user.get_first_name(), user.get_last_name(), user.get_e_mail(),
                               user.get_password(), user.get_course(), user.get_profile_picture(), admin, user.get_university_id()))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def update_user(self, user):
        query = """UPDATE user SET first_name=%s,last_name=%s,e_mail=%s,password=%s,course=%s
        ,profile_picture=FROM_BASE64(%s),admin=%s,university_id=%s WHERE id = %s"""
        duplicate_user = self.get_user_by_email(user.get_e_mail())
        if (duplicate_user is not None and duplicate_user.get_e_mail() != user.get_e_mail()):
            return False
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        if (user.get_admin()):
            admin = 1
        else:
            admin = 0
        cursor.execute(query, (user.get_first_name(), user.get_last_name(), user.get_e_mail(), user.get_password(),
                               user.get_course(), user.get_profile_picture(), user.admin, user.get_university_id(), user.get_id()))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def delete_user(self, id):
        query = """DELETE FROM user WHERE id=%s"""
        offer_ids = self.get_offer_ids_by_user_id(id)
        for offer_id in offer_ids:
            self.delete_offer(offer_id)
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        cursor.fetchall()
        rows = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()
        return rows > 0

    def get_all_universities(self):
        query = "SELECT id, university FROM university"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query)
        query_result = cursor.fetchall()
        result = []
        for element in query_result:
            result.append(data.university.University(*element))
        cursor.close()
        connection.close()
        return result

    def get_all_categories(self):
        query = "SELECT id, title FROM category"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query)
        query_result = cursor.fetchall()
        result = []
        for element in query_result:
            result.append(data.category.Category(*element))
        cursor.close()
        connection.close()
        return result

    def get_all_users(self):
        query = "SELECT first_name, last_name, e_mail, password, course, TO_BASE64(profile_picture), university_id, admin, id FROM user"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query)
        query_result = cursor.fetchall()
        result = []
        for element in query_result:
            first_name, last_name, e_mail, password, course, profile_picture, university_id, admin, id = element
            if(admin == 1):
                admin = True
            elif(admin == 0):
                admin = False
            user = data.user.User(
                first_name, last_name, e_mail, password, course, university_id, admin, id)
            user.set_profile_picture(profile_picture)
            result.append(user)
        cursor.close()
        connection.close()
        return result

    def get_university_by_name(self, name):
        query = "SELECT id, university FROM university WHERE university = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        university = data.university.University(*result)
        cursor.close()
        connection.close()
        return university

    def get_university_by_id(self, id):
        query = "SELECT id, university FROM university WHERE id = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        university = data.university.University(*result)
        cursor.close()
        connection.close()
        return university

    def get_category_by_name(self, name):
        query = "SELECT id, title FROM category WHERE title = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        category = data.category.Category(*result)
        cursor.close()
        connection.close()
        return category

    def get_category_by_id(self, id):
        query = "SELECT id, title FROM category WHERE id = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        category = data.category.Category(*result)
        cursor.close()
        connection.close()
        return category

    def get_offer_by_id(self, id):
        query_offer = "SELECT title,compensation_type,price,description,sold,category_id,user_id FROM offer WHERE id = %s"
        query_picture = "SELECT TO_BASE64(data) FROM picture WHERE offer_id = %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_offer, (id,))
        result = cursor.fetchone()
        if (result is not None):
            title, compensation_type, price, description, sold, category_id, user_id = result
            if(sold == 1):
                sold = True
            else:
                sold = False
            offer = data.offer.Offer(
                title, compensation_type, price, description, sold, category_id, user_id, id)
            cursor.execute(query_picture, (id,))
            result = cursor.fetchall()
            for element in result:
                unpacked_element, = element
                offer.add_picture(unpacked_element)
        else:
            offer = None
        cursor.close()
        connection.close()
        return offer

    def get_offer_ids_by_user_id(self, id):
        query_offer = "SELECT id FROM offer WHERE user_id = %s AND offer.sold <> 1"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_offer, (id,))
        result_tupel = cursor.fetchall()
        result = []
        for element in result_tupel:
            offer_id, = element
            result.append(offer_id)
        cursor.close()
        connection.close()
        return result

    def get_recommend_offer_ids_by_user(self, user):
        query_offer = "SELECT offer.id FROM offer,user WHERE offer.user_id = user.id AND user.university_id = %s AND offer.sold <> 1 AND offer.user_id <> %s"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_offer, (user.get_university_id(),user.get_id()))
        result_tupel = cursor.fetchall()
        result = []
        for element in result_tupel:
            offer_id, = element
            result.append(offer_id)
        cursor.close()
        connection.close()
        return result

    def get_recommend_offer_ids_without_user(self):
        query_offer = "SELECT offer.id FROM offer WHERE offer.sold <> 1 ORDER BY offer.id DESC LIMIT 0,10"
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_offer)
        result_tupel = cursor.fetchall()
        result = []
        for element in result_tupel:
            offer_id, = element
            result.append(offer_id)
        cursor.close()
        connection.close()
        return result

    def get_filtered_offer_ids(self, title, category, university, compensation_type, max_price, min_price):
        query_offer = """SELECT offer.id FROM offer,category,user,university 
        WHERE offer.category_id = category.id AND offer.user_id = user.id AND user.university_id = university.id 
        AND offer.sold <> 1 """
        value_list = []
        if (title is not None):
            value_list.append("%" + title + "%")
            query_offer += """AND offer.title LIKE %s """
        if (category is not None):
            value_list.append(category)
            query_offer += """AND category.title = %s """
        if (university is not None):
            value_list.append(university)
            query_offer += """AND university.university = %s """
        if (compensation_type is not None):
            value_list.append(compensation_type)
            query_offer += """AND offer.compensation_type = %s """
        if (max_price is not None):
            value_list.append(max_price)
            query_offer += """AND offer.price <= %s """
        if (min_price is not None):
            value_list.append(min_price)
            query_offer += """AND offer.price >= %s """
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_offer, tuple(value_list))
        result_tupel = cursor.fetchall()
        result = []
        for element in result_tupel:
            offer_id, = element
            result.append(offer_id)
        cursor.close()
        connection.close()
        return result

    def create_offer(self, offer):
        query_offer = """INSERT INTO 
        offer (title,compensation_type,price,description,sold,category_id,user_id) 
        VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        query_picture = """INSERT INTO picture (data,offer_id) VALUES (FROM_BASE64(%s),%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        if (offer.get_sold()):
            sold = 1
        else:
            sold = 0
        cursor.execute(query_offer, (offer.get_title(), offer.get_compensation_type(), offer.get_price(),
                                     offer.get_description(), sold, offer.get_category_id(), offer.get_user_id()))
        cursor.fetchall()
        cursor.execute("SELECT LAST_INSERT_ID()")
        id, = cursor.fetchone()
        for element in offer.get_pictures():
            cursor.execute(query_picture, (element, id))
        connection.commit()
        cursor.close()
        connection.close()
        return offer

    def update_offer(self, offer):
        query_offer = """UPDATE offer SET title=%s,compensation_type=%s,price=%s,description=%s,sold=%s,category_id=%s,user_id=%s WHERE id = %s"""
        query_delete_picture = """DELETE FROM picture WHERE offer_id= %s"""
        query_insert_picture = """INSERT INTO picture (data,offer_id) VALUES (FROM_BASE64(%s),%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        if (offer.get_sold()):
            sold = 1
        else:
            sold = 0
        cursor.execute(query_offer, (offer.get_title(), offer.get_compensation_type(),
                                     offer.get_price(), offer.get_description(), sold, offer.get_category_id(), offer.get_user_id(), offer.get_id()))
        cursor.fetchall()
        cursor.execute(query_delete_picture, (offer.get_id(),))
        cursor.fetchall()
        for picture in offer.get_pictures():
            cursor.execute(query_insert_picture, (picture, offer.get_id()))
            cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return offer

    def delete_offer(self, id):
        query_picture = """DELETE FROM picture WHERE offer_id=%s"""
        query_offer = """DELETE FROM offer WHERE id=%s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_picture, (id,))
        cursor.fetchall()
        cursor.execute(query_offer, (id,))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def add_watchlist_entry(self, watchlist_entry):
        query = """INSERT IGNORE INTO watchlist (user_id,offer_id) VALUES (%s,%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        cursor = connection.cursor()
        cursor.execute(query, (watchlist_entry.get_user_id(),
                       watchlist_entry.get_offer_id()))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def delete_watchlist_entry(self, watchlist_entry):
        query = """DELETE FROM watchlist WHERE user_id=%s AND offer_id=%s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (watchlist_entry.get_user_id(),
                       watchlist_entry.get_offer_id()))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def get_watchlist(self, user_id):
        query = """SELECT user_id,offer_id FROM watchlist WHERE user_id=%s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        result = []
        for element in cursor.fetchall():
            result.append(data.watchlist_entry.Watchlist_entry(*element))
        connection.commit()
        cursor.close()
        connection.close()
        return result

    def create_chat(self, chat):
        query_select = """SELECT id FROM chat WHERE user_id = %s AND offer_id = %s"""
        query_insert = """INSERT IGNORE INTO chat (user_id,offer_id) VALUES (%s,%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        cursor = connection.cursor()
        cursor.execute(query_select, (chat.get_user_id(), chat.get_offer_id()))
        result = cursor.fetchall()
        if (cursor.rowcount > 0):
            result, = result
            id, = result
        else:
            cursor.execute(query_insert, (chat.get_user_id(), chat.get_offer_id()))
            cursor.fetchall()
            cursor.execute("SELECT LAST_INSERT_ID()")
            id, = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return id

    def add_message(self, message):
        query = """INSERT INTO message (message,timestamp,user_id,chat_id) VALUES (%s,%s,%s,%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (message.get_text(),
                       message.get_timestamp(),
                       message.get_user_id(),
                       message.get_chat_id()))
        cursor.fetchall()
        cursor.execute("SELECT LAST_INSERT_ID()")
        id, = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return id

    def get_conversation(self, chat_id):
        query = """SELECT user_id, chat_id, message, timestamp, id FROM message WHERE chat_id = %s ORDER BY timestamp ASC"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (chat_id,))
        result = []
        for element in cursor.fetchall():
            result.append(data.message.Message(*element))
        connection.commit()
        cursor.close()
        connection.close()
        return result

    def delete_message(self, chat_id, message_id):
        query = """DELETE FROM message WHERE id=%s AND chat_id=%s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (message_id, chat_id))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def get_conversations(self, user_id):
        query = """SELECT DISTINCT chat.user_id, chat.offer_id, chat.id FROM chat, offer WHERE chat.user_id = %s OR (offer.id = chat.offer_id AND offer.user_id = %s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (user_id, user_id))
        result = []
        for element in cursor.fetchall():
            result.append(data.chat.Chat(*element))
        connection.commit()
        cursor.close()
        connection.close()
        return result

    def get_chat_by_id(self, chat_id):
        query = """SELECT DISTINCT chat.user_id, chat.offer_id, chat.id FROM chat WHERE id = %s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (chat_id,))
        result = data.chat.Chat(*cursor.fetchone())
        connection.commit()
        cursor.close()
        connection.close()
        return result

    def delete_chat(self, chat_id):
        query_message = """DELETE FROM message WHERE chat_id = %s"""
        query_chat = """DELETE FROM chat WHERE id = %s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query_message, (chat_id,))
        cursor.fetchall()
        cursor.execute(query_chat, (chat_id,))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def is_message_of_user(self, message_id, chat_id, user_id):
        query = """SELECT id FROM message WHERE id = %s AND chat_id = %s AND user_id = %s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (message_id, chat_id, user_id))
        cursor.fetchall()
        if (cursor.rowcount > 0):
            result = True
        else:
            result = False
        connection.commit()
        cursor.close()
        connection.close()
        return result

    def is_chat_of_user(self, chat_id, user_id):
        query = """SELECT chat.id FROM chat,offer WHERE chat.id = %s AND chat.user_id = %s OR (offer.id = chat.offer_id AND offer.user_id = %s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (chat_id, user_id, user_id))
        cursor.fetchall()
        if (cursor.rowcount > 0):
            result = True
        else:
            result = False
        connection.commit()
        cursor.close()
        connection.close()
        return result

    def create_rating(self, rating):
        query = """INSERT IGNORE INTO rating (rating,user_id_sender,user_id_receiver) VALUES (%s,%s,%s)"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        cursor = connection.cursor()
        cursor.execute(query, (rating.get_rating(
        ), rating.get_user_id_sender(), rating.get_user_id_receiver()))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def update_rating(self, rating):
        query = """UPDATE rating SET rating=%s WHERE user_id_sender = %s AND user_id_receiver = %s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (rating.get_rating(
        ), rating.get_user_id_sender(), rating.get_user_id_receiver()))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

    def get_average_rating(self, user_id):
        query = """SELECT AVG(rating) FROM rating WHERE user_id_receiver=%s GROUP BY user_id_receiver"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        rating = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if (rating is not None):
            rating, = rating
            return rating
        else:
            return 0

    def get_rating(self, user_id_sender,user_id_receiver):
        query = """SELECT rating, user_id_sender, user_id_receiver, id FROM rating WHERE user_id_sender=%s AND user_id_receiver=%s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (user_id_sender,user_id_receiver))
        rating = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if (rating is not None):
            return data.rating.Rating(*rating)
        else:
            return None

    def delete_rating(self, user_id_sender, user_id_receiver):
        query = """DELETE FROM rating WHERE user_id_sender = %s AND user_id_receiver = %s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        cursor.execute(query, (user_id_sender, user_id_receiver))
        cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
