from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from django import forms
import uuid
import random 
import string 

class USER(AbstractUser):
    LEVEL = [
        ('', 'Level'),
        ('Prep1', 'Prep1'),
        ('Prep2', 'Prep2'),
        ('Prep3', 'Prep3'),
        ('Sec1', 'Sec1'),
        ('Sec2', 'Sec2'),
        ('Sec3', 'Sec3'),
    ]

    def generate_unique_code():
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=5))

    username = models.CharField(default='New user', max_length=150, unique=True)
    Level = models.CharField(choices=LEVEL, max_length=50 , default='')
    unique_code = models.CharField(default=generate_unique_code, editable=False, unique=True, blank=True, max_length=5)
    user_class = models.TextField(max_length=50 , default='')

    def __str__(self):
        return f'{self.username} {self.user_class}({self.unique_code})'


class ACTIVITY(models.Model):
    title = models.TextField(max_length=50, default='new Activity')
    brief = models.TextField(max_length=70)
    details = models.TextField(max_length=500)
    def __str__(self):
        return f'{self.title}'

class SubscribeModel(models.Model):
    name = models.CharField(max_length=100)
    Code = models.CharField(max_length=10)
    user_class = models.CharField(max_length=100, null=True)
    activity = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}({self.activity})'


class PODCAST(models.Model):
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='courses/')

    def __str__(self):
        return f'{self.name}'


class NEWS(models.Model):
    title = models.CharField(max_length=50, null=True) 
    text = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return f'{self.text}'


class ARTICLE(models.Model):
    title = models.CharField(max_length=255)
    content = CKEditor5Field("Text", config_name="default")
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.title


class QUIZ(models.Model):
    title = models.ForeignKey(ARTICLE, on_delete=models.CASCADE)
    num_questions = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title.title


class QUESTION(models.Model):
    quiz = models.ForeignKey(QUIZ, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return f'{self.quiz}({self.id})'


class ANSWER(models.Model):
    question = models.ForeignKey(QUESTION, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text} - {self.text}"
