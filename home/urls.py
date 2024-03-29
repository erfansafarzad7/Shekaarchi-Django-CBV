from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), # {url 'home:home'}
    path('search/', views.ItemSearchView.as_view(), name='search'), # {url 'home:search'}

]
