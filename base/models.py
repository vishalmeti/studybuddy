from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    participants=models.ManyToManyField(User,related_name='participants',blank=True) #as user is already used for the host.. we have to specify the related name here in order to use it again

    desc=models.TextField(blank=True,null=True)#null=True means this value can be blank blank=true is for validation in the form... it is for the frontend
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.user)+' |  '+self.body[0:50]+'  -->  '+str(self.room))