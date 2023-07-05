import json
from json import JSONEncoder
import re
import uuid
import secrets
import random
import string


class PasswordValidationException(Exception):
    def __init__(self, data = "forbidden") -> None:
        self.data = data
        
    def __str__(self) -> str:
        return self.data
# print(uuid.uuid4())
class Encoder(JSONEncoder):
    def default(self, o):
        if type(o).__name__ == "UUID":
            return o.hex
        return o.__dict__
    
class NonUniqueException(Exception):
    def __init__(self, data) -> None:
        self.data = data
        
    def __str__(self) -> str:
        return self.data
class ForbiddenException(Exception):
    def __init__(self, data = "forbidden") -> None:
        self.data = data
        
    def __str__(self) -> str:
        return self.data

class Subject:
    def __init__(self, name, id_ = "".join([random.choice(string.hexdigits) for i in range(32)])):#= uuid.uuid4()) -> None:
        self.title = str(name)
        # print(id_) 

        self.id = uuid.UUID(id_) #uuid.uuid4() if not id_  else uuid.UUID(id_)
        
    def __repr__(self) -> str:
        return str(self.title)
    def serialize_to_json(self, json_file):
        with open(json_file, "w") as write_file:
            json.dump(self, write_file, cls=Encoder)

    @classmethod
    def serialize_list_to_json(cls, students, file):
        with open(file, "w") as write_file:
            json.dump(students, write_file, cls=Encoder)

class Score:
    def __init__(self, score, id_ = None, user_id = None) -> None:
        self.score = score
        
        self.subject_id = id_# if not id_ else uuid.UUID(id_)
        self.user_id = user_id #if not user_id else uuid.UUID(user_id)
        
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    def serialize_to_json(self, json_file):
        with open(json_file, "w") as write_file:
            json.dump(self, write_file, cls=Encoder)

    @classmethod
    def serialize_list_to_json(cls, students, file):
        with open(file, "w") as write_file:
            json.dump(students, write_file, cls=Encoder)
    def __str__(self) -> str:
        return (self.score)
 
class Role:
       Mentor = "Role.Mentor"
       Trainee = "Role.Trainee"

class User:

    def __init__(self, username, password, role,  id_ = "".join([random.choice(string.hexdigits) for i in range(32)])):# = uuid.uuid4()) -> None:
        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{6,}', password):
            raise PasswordValidationException
        self.username = username
        self.password = password
        self.role = role
        self.password = password 
        self.id = uuid.UUID(str(id_))
        self.subject = []
    
    def serialize_to_json(self, json_file):
        with open(json_file, "w") as write_file:
            json.dump(self, write_file, cls=Encoder)

    @classmethod
    def serialize_list_to_json(cls, students, file):
        with open(file, "w") as write_file:
            json.dump(students, write_file, cls=Encoder)
    @classmethod
    def create_user(cls, username,password, role):
        return cls(username, password, role)

    def add_score_for_subject(self, subject:Subject, score: Score):
        score = Score(score) if  type(score) is not Score else score
        # print(score)
        # print(type(score))
        score.user_id = self.id
        score.subject_id = subject.id
        self.subject.append({subject.title: score.score})
    def __repr__(self):
        return f"{self.username} with role {self.role}: {self.subject}"

def get_subjects_from_json(subjects_json):
    with open(subjects_json) as file:
        data = json.load (file)
    data = data if type(data) is list else [data]
    for i in range(len(data)):
        
        actual = data[i]
        data[i] = Subject(data[i].get("title")) 
        data[i].__dict__.update(actual)
    return data

def get_grades_from_json(grades_json):
    with open(grades_json) as file:
        data = json.load(file)
    data = data if type(data) is list else [data]
    for i in range(len(data)):
        actual = data[i]
        data[i] = Score(data[i].get("score"))
        data[i].__dict__.update(actual)
    return data

def get_users_from_json(users_json):
    with open(users_json) as file:
        data = json.load (file)
    data = data if type(data) is  list else [data]
    for i in range(len(data)):
        actual = data[i]
        data[i] = User(data[i].get("users_json"),data[i].get("password"),data[i].get("role")) 
        data[i].__dict__.update(actual)
    return data

def get_users_with_grades(users_json, subjects_json, grades_json):
    subjects = get_subjects_from_json(subjects_json)
    users = get_users_from_json(users_json)
    grades = get_grades_from_json(grades_json)
    for i in range(len(users)):
        for grade in grades:
            if users[i].id == grade.user_id:
                for subject in subjects:
                    if subject.id == grade.subject_id:
                        users[i].add_score_for_subject(subject, grade)
    return users
                
    

def check_if_user_present(user, password, users):
    if (user, password) not in [(x.username, x.password) for x in users]:
        return False
    return True
def add_user(user, users):
    if user.username not in [x.username for x in users]:
        users.append(user)
    else:
        raise NonUniqueException("User with name Mentor already exists") 

def add_subject(subject, subjects):
    if subject.title not in [x.title for x in subjects]:
        subjects.append(subject)

def get_grades_for_user(username:str, user:User, users:list):
    if username == user.username or user.role == Role.Mentor:
        return find_by_name(username, users).subject
    else:
        raise  ForbiddenException
def find_by_name(username, users):
    for i in users:
        if username == i.username:
            return i 


def users_to_json(users, json_file):
    User.serialize_list_to_json(users,json_file)


def subjects_to_json(subjects, json_file):
    Subject.serialize_list_to_json(subjects,json_file)

def grades_to_json(users, subjects, json_file):
    grades = []
    for user in users:
        for subject in user.subject:
            for sub in subjects:
                if subject == sub:
                    grades.append(user.subject[subject], user.id, sub.id)
    Score.serialize_list_to_json(grades,json_file)