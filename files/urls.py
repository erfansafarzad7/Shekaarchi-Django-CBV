from django.urls import path
from . import views


app_name = 'files'
urlpatterns = [
    path('<int:code>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('create/', views.ItemCreateView.as_view(), name='create'),
    path('delete-item/<int:code>', views.ItemDeleteView.as_view(), name='delete_item'),
    path('update-item/<int:code>', views.ItemUpdateView.as_view(), name='update_item'),
]
