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
from .filters import *
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import ListView,DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView

# Create your views here.
def home(request):
  bikes = Bikepost.objects.all()
  total_bikes=bikes.count()
  customer = Customer.objects.all()
  total_customer = customer.count()
  context={'total_bikes':total_bikes,'total_customer':total_customer}
  return render(request,'app/home.html',context)

def search_list(request):
  if request.method == 'POST':
    q = request.POST['q']
    bikes = Bikepost.objects.filter(bike_name__icontains=q)
    
    
  context = { 'q': q, 'bikes':bikes}
  return render(request,'app/search_list.html',context)


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
      messages.success(request,"Congratulations!!! Registered successfully Login Now")
      form.save()
      return redirect('login')
    return render(request, 'app/customerregistration.html',{'form':form})



class CustomerUpdateView(LoginRequiredMixin,UpdateView):
  model = Customer
  fields = ('first_name','last_name','profile_image','email','mobile','nid','photo_of_NID','driving_licence','Photo_of_licence','location')
  template_name = 'app/user_profile.html'
  login_url = 'login'

  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)

def profile(request,pk):
  customer = Customer.objects.get(user_id = request.user.id)
  post = Bikepost.objects.filter(post_user_id = request.user.id)
  posts=post.count()
  return render(request, 'app/customer_profile.html',{'customer':customer,'post':post,'posts':posts})

def customer_profile(request,pk):
  customer = Customer.objects.get(pk=pk)
  return render(request, 'app/customer_profile.html', {'customer':customer,})


def all_bikes(request):
  bikes = Bikepost.objects.all()
  myfilter = BikepostFilter(request.GET,queryset=bikes)
  bikes = myfilter.qs
  all_bike=bikes.count()
  customer = Customer.objects.all()
  all_cus=customer.count()
  page = Paginator(bikes, per_page=4)
  page_list = request.GET.get('page')
  page = page.get_page(page_list)
  rent_bike = Rentbike.objects.all()
  
  return render(request, 'app/all_bikes.html',{'bikes':bikes,'page':page,'myfilter': myfilter,'all_bike':all_bike,'all_cus':all_cus,'customer':customer,'rent_bike':rent_bike})

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
  fields = ('bike_images','bike_name','rent_price','bike_description','drop_off_location','is_available')
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


def rent_bike_form(request,pk):
  if request.method == 'POST':
    # obj= get_object_or_404(Rentbike,rent_user=request.user)
    form = RentBikeForm(request.POST)
    if form.is_valid():
      instance=form.instance.post_user = Bikepost.objects.get(pk=pk)
      instance.is_available = False
      instance = form.save(commit=False)
      instance.rent_user = request.user
      instance.save()
      messages.success(request, 'Congratulations Your request sent succesfully!!!')
  else:
    form = RentBikeForm()
  context = {'form':form, }
  return render(request,'app/rent_form.html',context)



def rent_details(request):
  rent_request= Rentbike.objects.all()
  return render(request, 'app/request.html',{'rent_request':rent_request,})

def rent_history(request):
  rent_history= Rentbike.objects.all()
  return render(request, 'app/rent_history.html',{'rent_history':rent_history,})


def cancelRequest(request,pk):
  # bike = Rentbike.objects.get(rent_user=rent_user)
  bike = get_object_or_404(Rentbike, id=pk)
  bike.delete()
  return redirect('home')
  # return render(request, 'app/rent_history.html', {'bike': bike})

def decline(request,pk):
  bike = get_object_or_404(Rentbike, pk=pk)
  bike.request_status = "Decline"
  bike.save()
  return redirect('home')
  # return render(request, 'app/request.html',{'bike':bike})

def accept(request,pk):
  bike = get_object_or_404(Rentbike, pk=pk)
  bike.request_status = "Accepted"
  bike.save()
  return redirect('home')
  # return render(request, 'app/request.html',{'bike':bike})