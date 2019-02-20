from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='')

    def __str__(self):
        return self.user.username


class Base(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255,)

    class Meta:
        abstract = True


class Category(Base):

    def __str__(self):
        return self.name


class SubCategory(Base):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Topic(Base):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    date_posted = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username + ' : ' + self.topic.name





