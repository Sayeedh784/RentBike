from http.client import HTTPResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from .form import *
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import ListView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView

# Create your views here.
def home(request):
  return render(request,'app/home.html')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'app/login.html',context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/login')

class CustomerRegistration(View):
  def get(self,request):
    form = CustomerRegistrationFrom()
    return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
    form = CustomerRegistrationFrom(request.POST)
    if form.is_valid():
      messages.success(request,"Congratulations!!! Registered successfully")
      form.save()
    return render(request, 'app/customerregistration.html',{'form':form})

def userprofileform(request,pk):
  if request.method == 'POST':
    obj = get_object_or_404(Customer, user_id=request.user.id)
    form = CustomerForm(request.POST, request.FILES, instance=obj)
    if form.is_valid():
      messages.success(request,'Congratulations profile Updated successfully!!!!')
      form.save()
      
  else:
    form = CustomerForm()
  context = {'form':form}
  return render(request, 'app/user_profile.html',context)


def profile(request,pk):
  customer = Customer.objects.get(user_id = request.user.id)
  post = Bikepost.objects.filter(post_user_id = request.user.id)
  return render(request, 'app/customer_profile.html',{'customer':customer,'post':post})

def customer_profile(request,pk):
  customer = Customer.objects.get(pk=pk)
  
  return render(request, 'app/customer_profile.html', {'customer':customer,})

# def bikepost(request):
#   if request.method == 'POST':
    
#     form=BikePostForm(request.POST,request.FILES)
#     if form.is_valid():
#       instance = form.save(commit=False)
#       instance.user = request.user
#       instance.save()
#       messages.success(request, 'Bike post succesfully!!')
      
#   else:
#     form = BikePostForm()
#   return render(request, 'app/bikepost.html',{'form':form})

def all_bikes(request):
  bikes = Bikepost.objects.all()
  return render(request, 'app/all_bikes.html',{'bikes':bikes})
# class BikeListView(LoginRequiredMixin,ListView):
#   model = Bikepost
#   template_name = 'app/all_bikes.html'
#   login_url = 'login'
class BikePostCreateView(LoginRequiredMixin,CreateView):
  model = Bikepost
  template_name = 'app/bikepost.html'
  fields = ('bike_images','bike_name','milage_covered','milagePerliter','bike_condition','rent_price','bike_description','drop_off_location','is_available')
  login_url = 'login'

  def form_valid(self, form):
    form.instance.post_user = self.request.user
    return super().form_valid(form)

class BikeDetailView(LoginRequiredMixin,DetailView):
  model = Bikepost
  template_name = 'app/bike_detail.html'
  login_url = 'login'

class PostUpdateView(LoginRequiredMixin,UpdateView):
  model = Bikepost
  fields = ('bike_images','bike_name','rent_price','bike_description','drop_off_location')
  template_name = 'app/post_edit.html'
  login_url = 'login'

  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.post_user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)

class PostDeleteView(LoginRequiredMixin,DeleteView):
  model = Bikepost
  template_name = 'app/post_delete.html'
  success_url = reverse_lazy('bikes')
  login_url = 'login'


  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.post_user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)