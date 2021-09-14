from django.db import models
from django.conf import settings
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.deletion import RESTRICT
from django.http.request import MediaType
from django.utils.text import slugify
from unidecode import unidecode
from django.db.models.signals import ModelSignal, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.utils import timezone
from django_quill.fields import QuillField
import uuid

class ContactLink(models.Model):
    email = models.CharField(max_length=200, null=True, default="")
    phone = models.CharField(max_length=200, null=True, default="")
    address = models.CharField(max_length=200, null=True, default="")
    codepen = models.CharField(max_length=200, null=True, default="")
    github = models.CharField(max_length=200, null=True, default="")
    twitter = models.CharField(max_length=200, null=True, default="")
    dribbble = models.CharField(max_length=200, null=True, default="")
    instagram = models.CharField(max_length=200, null=True, default="")
    linkdein = models.CharField(max_length=200, null=True, default="")
    facebook = models.CharField(max_length=200, null=True, default="")

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=200, null=True,  default="")
    email = models.CharField(max_length=100, null=True,  default="")
    suggestion = models.CharField(max_length=400, null=True, default="")
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Title(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class CustomFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name



class Note(models.Model):
    custom_folder = models.ForeignKey(CustomFolder, on_delete=models.CASCADE ,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=200)
    note_content = QuillField(blank=True, default="")
    image = models.ImageField(upload_to='note-images/',null=True, blank=True)
    video=models.FileField(upload_to='home_page_vidoes/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_favorite = models.BooleanField(default=False)
    at_dashboard = models.BooleanField(default=False)

    def __str__(self):
        return self.note_title

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    update_at = models.DateTimeField('Updated', auto_now=True)
    isCompleted = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class UserProfile(models.Model):  
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # USERNAME_FIELD = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=15,default="",  )
    linkedin = models.CharField(max_length=200, default="")  
    instagram = models.CharField(max_length=200, default="")  
    image = models.ImageField(default='profiles/default.jpg',upload_to='profiles/', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        new_user = UserProfile(user=instance)
        new_user.save()


class NewsLetters(models.Model):
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email

class FeedBack(models.Model):
    stars = models.IntegerField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.stars


class Testimonials(models.Model):
    name = models.CharField(max_length=200)
    post = models.CharField(max_length=300)
    facebook_link = models.URLField(default="", blank=True)
    instagram_link = models.URLField(default="", blank=True)
    twitter_link = models.URLField(default="", blank=True)
    linkedin_link = models.URLField(default="", blank=True)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.question
