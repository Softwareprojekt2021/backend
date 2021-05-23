

class University:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"""Universität
id: {self.id}
Name: {self.name}"""

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name