from tcidatabase.models import Token, User


def create_user():
    return User(firstname='fixtures').save()


def create_token():
    return Token(user=create_user()).save()
