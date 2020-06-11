from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index ),
    path(r'products/', views.index),

    re_path(r'^products\/(?:.*)/?$', views.index),
]