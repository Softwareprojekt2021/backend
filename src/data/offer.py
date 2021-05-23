import base64

class Offer:
    def __init__(self, title, compensation_type, price, description, sold = False, category_id = 0, user_id = 0, id = 0):
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
Bilddaten: {map(hex,self.pictures)}"""

    def get_id(self):
        return self.id
    def get_title(self):
        return self.title
    def get_compensation_type(self):
        return self.compensation_type
    def get_price(self):
        return self.price
    def get_description(self):
        return self.description
    def get_sold(self):
        return self.sold
    def get_category_id(self):
        return self.category_id
    def get_user_id(self):
        return self.user_id
    def get_pictures_binary(self):
        return self.pictures
    def get_pictures_base64(self):
        return map(lambda e : base64.b64encode(e).decode(),self.pictures)
    def add_picture_binary(self,picture):
        self.pictures.append(picture)
    def add_picture_base64(self,picture):
        self.pictures.append(base64.b64decode(picture))