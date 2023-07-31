from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):

    name = models.CharField(max_length=200 ,null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True,null=True)
    avatar = models.ImageField(null=True,default='avatar.svg')


    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

class Topic(models.Model):

  name = models.CharField(max_length=200)


  def __str__(self): 
     return self.name




class Room(models.Model):
    
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True) # takes a time stamp everytime the data is updated so basically
    #when the records is updated the column is updated to currenttimestamp
    created = models.DateTimeField(auto_now_add=True)  #timestamp is created when we create and save the instance 
    #for the first time and it does not update


    class Meta:
        
        ordering = ['-updated','-created']


    def __str__(self): 
        
        return self.name
    
 



class Message(models.Model):
    
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)#room get deleted all the message for that room is deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)

    class Meta():

        ordering = ['-updated','-created']

    def __str__(self): 
        
        return self.body[:50]

    