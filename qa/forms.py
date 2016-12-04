from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from qa.models import Question, Answer, Profile, Tag


class AskForm(forms.Form):
    title = forms.CharField(max_length=255, help_text='Topic', label='Title')
    text = forms.CharField(widget=forms.Textarea, help_text='Question body', label='Text')
    tags = forms.CharField(max_length=255, help_text='for example #ML #regression #NN', label='Tags')

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
        self.cleaned_data['author'] = Profile.objects.get(user=self._user)
        question = Question(**self.cleaned_data)
        for tag in self.cleaned_data['tags'].strip().split('#'):
            tag = tag.lower()
            Tag.objects.add(tag_name=tag, question=question)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Text is empty', code='validation_error')
        return text

    def clean_question(self):
        question = self.cleaned_data['question']
        if question == 0:
            raise forms.ValidationError('Question number incorrect', code='validation_error')
        return question

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(Question, pk=self.cleaned_data['question'])
        if self._user.is_anonymous():
            self.cleaned_data['author_id'] = 1
        else:
            self.cleaned_data['author'] = self._user

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



