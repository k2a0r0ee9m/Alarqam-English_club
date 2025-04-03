from django.contrib import admin
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django_ckeditor_5.widgets import CKEditor5Widget


class Signupform(UserCreationForm):
    class Meta:
        model = USER
        fields = ['username', 'password1', 'password2', 'Level','user_class']
        widgets = {'Level': forms.Select(attrs={'placeholder': 'Level'})}

class CustomLoginForm(forms.Form):
    unique_code = forms.CharField(max_length=5,required=True,widget=forms.TextInput(attrs={'placeholder': 'Code'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'new-password'}))


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribeModel
        fields = ['name', 'Code', 'activity']


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = ARTICLE
        fields = ['title', 'content']

class QuizForm(forms.ModelForm):
    class Meta:
        model = QUIZ
        fields = ['title', 'num_questions']

