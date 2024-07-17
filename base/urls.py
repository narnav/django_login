from django.contrib import admin
from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.index),
    path('test', views.test),
    path('pub', views.allpub),
    path('member', views.member),
    path('products/', views.product, name='product_list'),
    path('products/<int:id>/', views.product, name='product_detail'),
    path('books/', views.book_view),
    path('books/<int:id>/', views.book_view),
    path('login/', TokenObtainPairView.as_view()),
    path('register/', views.register),
]
