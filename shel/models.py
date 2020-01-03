from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, related_name="userProfile")
    displayed_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media', blank="True", null=True)

    def __str__(self):              # __unicode__ on Python 2
        return '{}'.format(self.displayed_name)


class Group(models.Model):

    name = models.CharField(max_length=128)
    admin = models.ForeignKey(Person, related_name='groupadmin')

    def __str__(self):              # __unicode__ on Python 2
        return '{}'.format(self.name)

class Membership(models.Model):
    person = models.ForeignKey(Person, related_name='groupmember')
    group = models.ForeignKey(Group, related_name='groupid')
    isAccepted = models.BooleanField()

    def __str__(self):              # __unicode__ on Python 2
        return '{}'.format(self.person.displayed_name)


class Post(models.Model):
    text = models.TextField()
    date = models.DateField()
    creator = models.ForeignKey(Person)
    group = models.ForeignKey(Group, related_name='groupname')

    def __str__(self):              # __unicode__ on Python 2
        return '{} - {} - {}'.format(self.group, self.creator, self.date)


class visitedPost(models.Model):
    member = models.ForeignKey(Person)
    post = models.ForeignKey(Post, related_name='visited')

    def __str__(self):              # __unicode__ on Python 2
        return '{} - {}'.format(self.member.displayed_name, self.post.date)