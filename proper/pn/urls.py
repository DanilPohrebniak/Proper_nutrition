from django.urls import path
from . import views

urlpatterns = [
    path('reference_tables/', views.reference_tables, name='reference_tables'),
    path('display_table/<str:model_name>/', views.display_table, name='display_table'),
    path('add_item/<str:model_name>/', views.add_item_view, name='add_item_view'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_item_view, name='delete_item_view'),
    path('edit/<str:model_name>/<int:pk>/', views.edit_item_view, name='edit_item_view'),
]