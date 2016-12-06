from random import randrange, shuffle

from django.core.management.base import BaseCommand
from qa.management.commands import _namegen

from qa.forms import SignUpForm, AskForm, AnswerForm, ProfileForm
from qa.management.commands import _textgen
from qa.models import Profile, Question


class Command(BaseCommand):
    help = "Generates things"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        usernames = []

        for i in range(30):
            username, first_name, last_name, email = _namegen.generate()

            try:
                form = SignUpForm(data={
                    "login": username,
                    "email": email,
                    "password": "changeme",
                    "password_again": "changeme",
                })

                if form.is_valid():
                    form.save()

                    if first_name != "":
                        form = ProfileForm(data={
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                            "about_me": _textgen.generate(2, 5),
                            "avatar": None,
                        })
                        print(form)
                        print(form.is_valid())
                        if form.is_valid():
                            profile = form.save(Profile.objects.profile_str(username))
                            profile.avatar = randrange(1, 13)
                            profile.save()
                            print(profile.first_name)
                    usernames.append(username)
            except Exception:
                pass

        questions = []

        for j in range(len(usernames)):
            for i in range(randrange(5, 40)):
                try:
                    shuffle(usernames)
                    username = usernames[0]

                    form = AskForm(data={
                        "title": _textgen.generate(1, 2, True),
                        "text": _textgen.generate(3, 7),
                        "tags": _textgen.generate_tags(),
                    })


                    if form.is_valid():
                        form.profile_user = Profile.objects.profile_str(username=username)
                        question = form.save()
                        question.rating = randrange(-20, 20)
                        question.save()
                        pk = question.pk
                        questions.append(pk)

                except Exception:
                    pass
        print(questions)
        for username in usernames:
            for i in range(randrange(5, 15)):
                shuffle(questions)
                question = Question.objects.get(pk=questions[0])

                form = AnswerForm(data={
                    "text": _textgen.generate(3, 7),
                    "question": question.pk
                })

                if form.is_valid():
                    form.profile_user = Profile.objects.profile_str(username)
                    form.save()
