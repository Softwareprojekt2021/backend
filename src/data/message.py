

class Message:
    def __init__(self, user_id, chat_id, text, timestamp, id=0):
        self.id = id
        self.user_id = user_id
        self.chat_id = chat_id
        self.text = text
        self.timestamp = timestamp

    def __str__(self):
        return f"""Message
Id: {self.id}
user id: {self.user_id}
chat id: {self.chat_id}
Text: {self.text}
Timestamp: {self.timestamp}"""

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_chat_id(self):
        return self.chat_id

    def get_text(self):
        return self.text

    def get_timestamp(self):
        return self.timestamp
