from django.db import models
from django.contrib.auth.models import User



class Topic(models.Model):
    name = models.CharField(max_length=100)
    rooms_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.name




class Room(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(User , on_delete=models.CASCADE , null = True ,blank=True)
    topic =models.ForeignKey(Topic, on_delete= models.CASCADE , default= "no topic") 
    popularity = models.IntegerField(default=0)
    name = models.CharField(max_length=200 , unique=True)
    description = models.TextField(max_length=300, null=True , blank=True)
    participants = models.ManyToManyField(User ,related_name = 'participant' , blank=True)
    # participants_count = models.IntegerField(defalut =0) todo
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    user =  models.ForeignKey(User , on_delete=models.CASCADE , default= "no user")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField(max_length=300, null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.text[0:50]
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, null=True , blank=True)
    profile_pic = models.ImageField(default = 'avatar.svg' , upload_to = 'images/')
    def __str__(self):
        return str(self.user)