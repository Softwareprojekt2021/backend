

class Rating:
    def __init__(self, rating, comment, user_id, id = 0):
        self.id = id
        self.rating = rating
        self.comment = comment
        self.user_id = user_id

    def __str__(self):
        return f"""Bewertung
id: {self.id}
Bewertung: {self.rating}
Kommentar: {self.comment}
user id: {self.user_id}"""

    def get_id(self):
        return self.id

    def get_rating(self):
        return self.rating

    def get_comment(self):
        return self.comment

    def get_user_id(self):
        return self.user_id