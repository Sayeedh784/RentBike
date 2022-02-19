from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE)
  first_name=models.CharField(max_length=30,blank=True,null=True)
  last_name=models.CharField(max_length=30,blank=True,null=True)
  mobile=models.CharField(max_length=30,blank=True,null=True)
  email=models.EmailField(max_length=20,blank=True,null=True)
  nid=models.IntegerField(blank=True,null=True)
  photo_of_NID=models.ImageField(upload_to='images/')
  driving_licence=models.CharField(max_length=100,blank=True,null=True)
  Photo_of_Licence=models.ImageField(upload_to='images/')
  Profile_image = models.ImageField(upload_to='images/')
  location=models.CharField(max_length=100,blank=True,null=True)

  def __str__(self):
    return str(self.id)

class Bikepost(models.Model):
  post_user = models.ForeignKey(Customer,on_delete=models.CASCADE)
  bike_images = models.ImageField(upload_to='images/',blank=True,null=True)
  bike_name = models.CharField(max_length=50,blank=True,null=True)
  rent_price = models.CharField(max_length=20,blank=True,null=True)
  bike_description = models.TextField(max_length=500,blank=True,null=True)
  drop_off_location = models.CharField(max_length=100,blank=True,null=True) 

  def __str__(self):
    return str(self.id)

class Rentbike(models.Model):
  rent_user= models.ForeignKey(Customer,on_delete=models.CASCADE)
  pick_up_location = models.CharField(max_length=100,blank=True,null=True)  
  drop_off_location = models.CharField(max_length=100,blank=True,null=True)
  pick_up_date = models.DateField()  
  drop_off_date = models.DateField()
  pick_up_time=models.TimeField() 

  