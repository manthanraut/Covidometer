from django.urls import path
from . import views
urlpatterns = [
path('',views.home,name="first"),
path('results',views.search,name="result")
]