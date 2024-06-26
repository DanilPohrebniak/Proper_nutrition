from django.urls import path
from . import views

urlpatterns = [
    path('reference_tables/', views.reference_tables, name='reference_tables'),
    path('display_table/<str:model_name>/', views.display_table, name='display_table'),
    path('add_item/<str:model_name>/', views.add_item_view, name='add_item_view'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_item_view, name='delete_item_view'),
    path('edit/<str:model_name>/<int:pk>/', views.edit_item_view, name='edit_item_view'),
    path('documents/', views.display_documents, name='display_documents'),
    path('add_doc/', views.add_document_view, name='add_document_view'),
    path('edit_doc/<int:pk>/', views.edit_document_view, name='edit_document_view'),
    path('delete_doc/<int:pk>/', views.delete_document_view, name='delete_document_view'),
    path('display_dishes/', views.display_dishes, name='display_dishes'),
    path('add_dish/', views.add_dish_view, name='add_dish_view'),
    path('edit_dish/<int:pk>/', views.edit_dish_view, name='edit_dish_view'),
    path('delete_dish/<int:pk>/', views.delete_dish_view, name='delete_dish_view'),
]