from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_user', views.process_user),
    path('success', views.success),
    path('login_user', views.login),
    path('logout', views.logout),
]
