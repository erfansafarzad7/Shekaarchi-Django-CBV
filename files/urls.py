from django.urls import path
from . import views


app_name = 'files'
urlpatterns = [
    path('<int:code>/', views.ItemDetailView.as_view(), name='item_detail'), # {url 'files:item_detail' code}
    path('create/', views.ItemCreateView.as_view(), name='create'), # {url 'files:create'}
    path('delete-item/<int:code>/', views.ItemDeleteView.as_view(), name='delete_item'), # {url 'files:delete_item' code}
    path('edit-item/<int:code>/', views.ItemUpdateView.as_view(), name='edit_item'), # {url 'files:edit_item' code}
    path('delete-image/<int:code>/<str:name>', views.DeleteImageView.as_view(), name='delete_image'), # {url 'files:delete_image' code name}
]
