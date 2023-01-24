from django.urls import path
from . import views


app_name = 'files'
urlpatterns = [
    path('<int:code>/', views.ItemDetailView.as_view(), name='item_detail'),

]