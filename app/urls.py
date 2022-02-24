
from unicodedata import name
from django.urls import path
from . import views
from .views import *
from .form import *
from django.contrib.auth import views as auth_views

urlpatterns=[
  path('',views.home,name="home"),
  path('profileform/<str:pk>/',views.userprofileform,name="profileform"),
  path('customer-profile/<str:pk>/',views.customer_profile,name="customer-profile"),
  path('profile/<str:pk>/',views.profile,name="profile"),
  
  path('bikepost/',views.BikePostCreateView.as_view(),name='bikepost'),
  path('bike-detail/<int:pk>/',BikeDetailView.as_view(), name='bike-detail'),
  path('post/<int:pk>/edit/',PostUpdateView.as_view(), name='post_edit'),
  
  path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post_delete'),
  path('bikes/',views.all_bikes,name="bikes"),
#   path('bike-list/',views.BikeListView.as_view(),name="bike-list"),

  path('registration/',views.CustomerRegistration.as_view(),name="registration"),
  path('login/',views.login_request, name='login'),
  path('logout/',views.logout_view, name='logout'),
  path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,
  success_url='/passwordchangedone/'), name='passwordchange'),
  path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),
        name='passwordchangedone'),
        
  path('password-reset/', auth_views.PasswordResetView.
        as_view(template_name='app/password_reset.html',
                form_class=MyPasswordResetForm), name='password_reset'),

  path('password-reset/done/', auth_views.PasswordResetDoneView.
        as_view(template_name='app/password_reset_done.html'),
        name='password_reset_done'),

  path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.
        as_view(template_name='app/password_reset_confirm.html',
                form_class=MySetPasswordForm),
        name='password_reset_confirm'),

  path('password-reset-complete/', auth_views.PasswordResetCompleteView.
        as_view(template_name='app/password_reset_complete.html'),
        name='password_reset_complete'),
    
] 
