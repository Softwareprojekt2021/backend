import mysql.connector

import data.user
import data.university
import data.category
import data.offer


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
        VALUES (%s,%s,%s,%s,%s,FROM_BASE64(%s),%s,%s);"""
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
        print(cursor.statement)
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
        query_offer = "SELECT id FROM offer WHERE user_id = %s"
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

    def create_offer(self, offer):
        query_offer = """INSERT INTO 
        offer (title,compensation_type,price,description,sold,category_id,user_id) 
        VALUES (%s,%s,%s,%s,%s,%s,%s);"""
        query_picture = """INSERT INTO 
        picture (data,offer_id) 
        VALUES (FROM_BASE64(%s),%s);"""
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
        cursor.execute("SELECT LAST_INSERT_ID();")
        id, = cursor.fetchone()
        print(id)
        for element in offer.get_pictures():
            cursor.execute(query_picture, (element, id))
        connection.commit()
        cursor.close()
        connection.close()
        return offer

    def update_offer(self, offer):
        query = """UPDATE offer SET title=%s,compensation_type=%s,price=%s,description=%s,sold=%s,category_id=%s,user_id=%s WHERE id = %s"""
        connection = mysql.connector.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, raise_on_warnings=True)
        cursor = connection.cursor()
        if (offer.get_sold()):
            sold = 1
        else:
            sold = 0
        cursor.execute(query, (offer.get_title(), offer.get_compensation_type(),
                               offer.get_price(), offer.get_description(), sold, offer.get_category_id(), offer.get_user_id(), offer.get_id()))
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
