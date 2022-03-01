
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator,MinLengthValidator
# Create your models here.

class User(AbstractUser):
  is_customer = models.BooleanField(default=False)

class Customer(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  first_name=models.CharField(max_length=30,blank=True,null=True)
  last_name=models.CharField(max_length=30,blank=True,null=True)
  mobile = models.CharField(validators=[MinLengthValidator(11), MaxLengthValidator(11)],max_length=11,blank=True,null=True)
  email=models.EmailField(max_length = 50,blank=True,null=True)
  nid=models.IntegerField(blank=True,null=True)
  photo_of_NID=models.ImageField(upload_to='images',null=True,blank=True)
  driving_licence=models.CharField(max_length=100,blank=True,null=True)
  Photo_of_licence=models.ImageField(upload_to='images',null=True,blank=True)
  profile_image = models.ImageField(upload_to='images',null=True,blank=True)
  location=models.CharField(max_length=100,blank=True,null=True)

  def __str__(self):
    return str(self.id)

CONDITION=(
  ('Old','Old'),
  ('Average','Average'),
  ('New','New'),
)

class Bikepost(models.Model):
  post_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
  bike_id = models.AutoField
  bike_images = models.ImageField(upload_to='images',blank=True,null=True)
  bike_name = models.CharField(max_length=50,blank=True,null=True)
  rent_price = models.CharField(max_length=20,blank=True,null=True)
  milage_covered = models.IntegerField(blank=True,null=True)
  milagePerliter = models.IntegerField(blank=True,null=True)
  bike_condition = models.CharField(max_length=100,choices=CONDITION,blank=True,null=True)
  bike_description = models.TextField(max_length=500,blank=True,null=True)
  drop_off_location = models.CharField(max_length=100,blank=True,null=True) 
  is_available = models.BooleanField(default=True)
  

  def get_absolute_url(self):
    return reverse('bike-detail', args=[str(self.id)])

class Rentbike(models.Model):
  rent_user= models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  post_user = models.ForeignKey(Bikepost,on_delete=models.CASCADE,null=True,blank=True)
  pick_up_location = models.CharField(max_length=100,blank=True,null=True)  
  drop_off_location = models.CharField(max_length=100,blank=True,null=True)
  pick_up_date = models.DateField()  
  drop_off_date = models.DateField()
  pick_up_time=models.TimeField() 
  request_status = models.CharField(max_length=30,default="Pending")
  

  def __str__(self):
    return str(self.id)


  