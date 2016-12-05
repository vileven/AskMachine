from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from qa.models import Question, Answer, Profile, Tag
from re import sub


class AskForm(forms.Form):
    title = forms.CharField(max_length=255, help_text='Topic', label='Title', required=False)
    text = forms.CharField(widget=forms.Textarea, help_text='Question body', label='Text', required=False)
    tags = forms.CharField(max_length=255, help_text='for example #ML #regression #NN', label='Tags', required=False)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip() == '':
            raise forms.ValidationError('Title is empty', code='validation_error')
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Text is empty', code='validation_error')
        return text

    def save(self):
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'],
                            author=self.profile_user, short_text=Question.cut_text(self.cleaned_data['text']))
        question.save()

        self.profile_user.questions_count += 1
        self.profile_user.save()

        tags = self.cleaned_data["tags"].replace(",", " ")
        tags = sub(r"[^\w\s]", "", tags)
        tags = sub(r"\s+", " ", tags)
        for tag in tags.split(" "):
            Tag.objects.add(tag_name=tag, question=question)

        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, help_text='Type your answer')
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Text is empty', code='validation_error')
        return text

    def clean_question(self):
        question = self.cleaned_data['question']
        if question <= 0:
            raise forms.ValidationError('Question number incorrect', code='validation_error')
        return question

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(Question, pk=self.cleaned_data['question'])
        # if self._user.is_anonymous():
        #     self.cleaned_data['author_id'] = 1
        # else:
        #     self.cleaned_data['author'] = self._user

        self.cleaned_data['author'] = self.profile_user

        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignUpForm(forms.Form):
    login = forms.CharField(label='Login', help_text='Your Login, max – 100 characters',
                            max_length=100, widget=forms.TextInput, required=False)

    email = forms.EmailField(label='Email', help_text='example@mail.com', max_length=30,
                             widget=forms.EmailInput, required=False)
    password = forms.CharField(label="Password", min_length=5, max_length=30,
                               help_text='5 to 30 characters, one digit and one letter',
                               widget=forms.PasswordInput, required=False)
    # password.type = 'password'

    password_again = forms.CharField(label='Repeat password', min_length=5, max_length=30,
                                     help_text='password again',
                                     widget=forms.PasswordInput, required=True)

    def clean_login(self):
        login = self.cleaned_data['login']
        if login.strip() == '':
            raise forms.ValidationError('Login is empty', code='validation_error')
        if Profile.objects.has(login):
            raise forms.ValidationError('This login has been already used!')
        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Email is empty', code='validation_error')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')

        return password

    def clean(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("password_again"):
            raise forms.ValidationError("Password mismatch!")

        return self.cleaned_data

    def save(self):
        # user = User.objects.create_user(**self.cleaned_data)
        user = User.objects.create_user(username=self.cleaned_data['login'], email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'])
        profile = Profile(user=user)
        profile.save()
        return profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    user = None

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        return password

    def clean(self):
        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError("Wrong login or password, try again!", code='validation_error')
        self.user = user
        return self.cleaned_data

    def save(self):
        return self.user


class ProfileForm(forms.Form):
    email = forms.EmailField(label='Email', help_text='example@mail.com', max_length=30,
                             widget=forms.EmailInput, required=False)
    first_name = forms.CharField(label='First name', help_text='Ivan', required=False, max_length=30)

    last_name = forms.CharField(label='Last name', help_text='Ivanov', required=False, max_length=30)

    about_me = forms.CharField(label='About me', help_text='I want to be a cosmonaut', required=False, max_length=2000)

    avatar = forms.ImageField(label='Avatar', required=False)
                              # widget=forms.FileInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Email is empty', code='validation_error')
        return email

    @staticmethod
    def load(profile):
        form = ProfileForm(initial={
            'email': profile.user.email,
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "about_me": profile.about_me,
        })
        return form

    def save(self, profile):
        profile.user.email = self.cleaned_data['email']
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.save()

        profile.about_me = self.cleaned_data['about_me']
        if self.cleaned_data['avatar'] is not None:
            profile.avatar = self.cleaned_data['avatar']
        profile.save()





