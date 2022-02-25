from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.db import transaction
from django.forms import fields, widgets
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, AuthenticationForm, UsernameField
PasswordChangeForm, PasswordResetForm, SetPasswordForm


class CustomerRegistrationFrom(UserCreationForm):
  password1 = forms.CharField(label='Password',widget=forms.
  PasswordInput(attrs={'class':'form-control'}))
  password2 = forms.CharField(label='Comfrim Password',widget=forms.
  PasswordInput(attrs={'class':'form-control'}))
  email = forms.CharField(required=True,widget=forms.
  EmailInput(attrs={'class':'form-control'}))

  class Meta:
    model=User
    fields = ['username','email','password1','password2']
    labels ={'email': 'Email'}
    widgets  = {'username':forms.TextInput(attrs=
    {'class':"form-control"})}

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.is_customer = True
    
    user.save()
    customer = Customer.objects.create(user=user)
    customer.email = self.cleaned_data.get('email')
    customer.save()
    return user

class CustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['first_name','last_name','profile_image','email','mobile','nid','photo_of_NID','driving_licence','Photo_of_licence','location']

class BikePostForm(forms.ModelForm):
  class Meta:
    model = Bikepost
    fields = ['bike_images','bike_name','rent_price','bike_description','drop_off_location']
    

class RentBikeForm(forms.ModelForm):
  class Meta:
    model = Rentbike
    exclude= ('rent_user','post_user','request_status',)
    # fields = ['pick_up_location','drop_off_location','pick_up_date','drop_off_date','pick_up_time']

class MyPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(label=_("Old Password"),
  strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,
 'class': 'form-control'}))
  new_password1 = forms.CharField(label=_("New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'New password',
  'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
  new_password2 = forms.CharField(label=_("Confrim New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
  'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
  email  = forms.EmailField(label=_("Email"),max_length=254,
  widget=forms.EmailInput(attrs={'autocomplete':'email',
  'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
  new_password1= forms.CharField(label=_("New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
  'class':'form-control'}),help_text=password_validation.
  password_validators_help_text_html())
  new_password2= forms.CharField(label=_("Comfrim New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
  'class':'form-control'}))