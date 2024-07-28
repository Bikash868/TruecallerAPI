from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone_number = models.IntegerField(null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    spam = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(unique=True, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    spam = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user)
    
class MatchUserContact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=False, blank=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.user)+' '+ str(self.contact)
