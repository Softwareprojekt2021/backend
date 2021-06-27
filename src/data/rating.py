

class Rating:
    def __init__(self, rating, user_id_sender, user_id_receiver, id=0):
        self.id = id
        self.rating = rating
        self.user_id_sender = user_id_sender
        self.user_id_receiver = user_id_receiver

    def __str__(self):
        return f"""Bewertung
id: {self.id}
Bewertung: {self.rating}
sender user id: {self.user_id_sender}
receiver user id: {self.user_id_receiver}"""

    def get_id(self):
        return self.id

    def get_rating(self):
        return self.rating

    def get_user_id_sender(self):
        return self.user_id_sender

    def get_user_id_receiver(self):
        return self.user_id_receiver
