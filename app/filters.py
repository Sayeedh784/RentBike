from django.forms import fields, forms
import django_filters
from .models import *


class BikepostFilter(django_filters.FilterSet):
  class Meta:
    model = Bikepost
    fields = ('rent_price','bike_condition','drop_off_location')