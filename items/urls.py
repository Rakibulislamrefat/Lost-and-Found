from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/my/', views.my_items, name='my_items'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('items/<int:pk>/claim/', views.submit_claim, name='submit_claim'),
    path('items/<int:pk>/claims/', views.manage_claims, name='manage_claims'),
    path('claims/<int:pk>/update/', views.update_claim, name='update_claim'),
]
