import base64


class User:
    def __init__(self, first_name, last_name, e_mail, password, course, university_id, admin=False, id=0):
        self.first_name = first_name
        self.last_name = last_name
        self.e_mail = e_mail
        self.password = password
        self.course = course
        self.profile_picture = None
        self.university_id = university_id
        if(admin is not None):
            self.admin = admin
        else:
            self.admin = False
        self.id = id

    def __str__(self):
        return f"""User
id: {self.id}
Vorname: {self.first_name}
Nachname: {self.last_name}
E-Mail: {self.e_mail}
Password: {self.password}
Kurs: {self.course}
Profilbild: {self.profile_picture}
Admin: {self.admin}
Uni_id: {self.university_id}"""

    def get_id(self):
        return self.id

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_e_mail(self):
        return self.e_mail

    def set_e_mail(self, e_mail):
        self.e_mail = e_mail

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_course(self):
        return self.course

    def set_course(self, course):
        self.course = course

    def get_profile_picture(self):
        return self.profile_picture

    def set_profile_picture(self, profile_picture):
        if (profile_picture is not None):
            self.profile_picture = profile_picture.replace("\n", "")
        else:
            self.profile_picture = None

    def get_admin(self):
        return self.admin

    def set_admin(self, admin):
        self.admin = admin

    def get_university_id(self):
        return self.university_id

    def set_university_id(self, university_id):
        self.university_id = university_id
