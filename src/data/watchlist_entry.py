

class Watchlist_entry:
    def __init__(self, user_id, offer_id):
        self.user_id = user_id
        self.offer_id = offer_id

    def __str__(self):
        return f"""Bewertung
user id: {self.user_id}
offer id: {self.offer_id}"""

    def get_user_id(self):
        return self.user_id

    def get_offer_id(self):
        return self.offer_id
