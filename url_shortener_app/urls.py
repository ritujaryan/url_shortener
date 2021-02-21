from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.shorten),
    path('short/', views.shorten),
    path('redirect/<slug:link>/', views.redirect_url),
    path('analytics/', views.get_analytics),
    path('views/', views.get_views),
    path('thanks/', views.thanks),
    path('image/', views.sendLogo),
    path('gif/', views.sendgif),
    path('icon/', views.sendicon),
    path('getlogo/', views.getLogo),
    path('getbg/', views.getbg),
    path('getbg2/', views.getbg2),
]