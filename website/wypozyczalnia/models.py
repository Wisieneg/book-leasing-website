from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone

CAT_CHOICES=[
    ('Thriller','Thriller'),
    ('Horror','Horror'),
    ('Fantastyka','Fantastyka'),
    ('Science-fiction','Science-fiction'),
    ('Obyczajowe','Obyczajowe'),
    ('Biografia','Biografia'),
    ('Reportaż','Reportaż'),
    ('Popularnon','Popularnon'),
]

class book(models.Model):
    title=models.CharField(max_length=80)
    author=models.CharField(max_length=50)
    release=models.IntegerField()
    pages=models.IntegerField()
    category=models.CharField(max_length=40,choices=CAT_CHOICES)
    amount=models.IntegerField()
    icon=models.ImageField(upload_to='images/')
    pub_date=models.DateTimeField(auto_now_add=True)
    info=models.TextField(default="")
    def __str__(self):
        return self.title+" author: "+self.author+"     amount: "+str(self.amount)

    def data(self):
        return datetime.strftime(self.pub_date,"%Y-%m-%d")

class lease(models.Model):
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(book,on_delete=models.CASCADE)
    data=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.client)+"    book: "+self.book.title