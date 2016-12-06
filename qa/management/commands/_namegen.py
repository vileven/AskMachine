from random import shuffle, randrange

from qa.management.commands._util import chance

first_names = [
    'Sergey', 'Max', 'Andrew', 'Jacob', 'Vladimir', 'Petr',
    'Uber', 'Escobar', 'Aleksey', 'Harry', 'Ron', 'Richard',
    'Cristiano', 'Lionel', 'Frank', 'Genry', 'Drako', 'Ricky',
    'Rick', 'Grigoriy', 'Ivan', 'Romeo', 'Albus', 'Dmitriy', 'Donald'
]

last_names = [
    'Volodin', 'Potter', 'Bekker', 'Peshkov', 'Gourenko', 'Ivanov',
    'Wysly', 'Dambldor', 'Malfoy', 'Samarev', 'Vasneczov', 'Lampard',
    'Ronaldo', 'Messi', 'Li', 'Putin', 'Putout', 'Smal', 'Knut', 'Trump'
    'Clinton', 'Petrov', 'Bauman', 'Lomonosov'
]


emails = [
    '@gmail.com', '@mail.ru', '@icloud.com', '@yandex.ru'
]


def generate_email(name):
    shuffle(emails)
    return name + emails[0]


def generate():
    shuffle(first_names)
    shuffle(last_names)
    first_name = first_names[0]
    last_name = last_names[0]
    username = first_name

    if chance(40):
        username = username.lower()

    if chance(40):
        if chance(50):
            username += "_"
        username += last_name

    username += str(randrange(1970, 2005))

    if chance(85):
        return username, first_name, last_name, generate_email(username)
    return username, "", "", generate_email(username)