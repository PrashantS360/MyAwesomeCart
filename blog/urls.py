from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="blogHome"),
    path('search/', views.search, name="BlogSearch"),
    path('blogpost/<int:id>', views.blogpost, name="blogPost")
]