# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
#Database for polls 

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.TextField(max_length=500, blank=True)
	name = models.CharField(max_length=50, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Question(models.Model):
	content = models.CharField(max_length=200)
	category = models.CharField(max_length=30, null=True)
	time = models.DateTimeField('date asked')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
	followers = models.ManyToManyField(User, related_name="followers")
	def __str__(self):
		return self.content

class Answer(models.Model):
	content = models.CharField(max_length=1000)
	time = models.DateTimeField('date answered')
	accepted = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	voters = models.ManyToManyField(User, related_name="voters")
	def __str__(self):
		return self.content[:50]

class Comment(models.Model):
	time = models.DateTimeField('date replied')
	content = models.CharField(max_length=1000)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

	def __str__(self):
		return self.content[:50]

