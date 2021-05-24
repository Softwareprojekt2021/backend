import base64


class Offer:
    def __init__(self, title, compensation_type, price, description, sold=False, category_id=0, user_id=0, id=0):
        self.title = title
        self.compensation_type = compensation_type
        self.price = price
        self.description = description
        self.sold = sold
        self.category_id = category_id
        self.user_id = user_id
        self.id = id
        self.pictures = []

    def __str__(self):
        return f"""Offer
id: {self.id}
Titel: {self.title}
Gegenleistung: {self.compensation_type}
Preis: {self.price}
Beschreibung: {self.description}
Verkauft?: {self.sold}
Kategorie id: {self.category_id}
User id: {self.user_id}
Bilddaten: {self.get_pictures_base64()}"""

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title
    
    def set_title(self,title):
        self.title = title

    def get_compensation_type(self):
        return self.compensation_type

    def set_compensation_type(self,compensation_type):
        self.compensation_type = compensation_type

    def get_price(self):
        return self.price
    
    def set_price(self,price):
        self.price = price

    def get_description(self):
        return self.description
    
    def set_description(self,description):
        self.description = description

    def get_sold(self):
        return self.sold
    
    def set_sold(self,sold):
        self.sold = sold

    def get_category_id(self):
        return self.category_id
    
    def set_category_id(self,category_id):
        self.category_id = category_id

    def get_user_id(self):
        return self.user_id

    def get_pictures(self):
        return self.pictures


    def add_picture(self, picture):
        self.pictures.append(picture)

    def clear_picture(self):
        self.pictures = []
