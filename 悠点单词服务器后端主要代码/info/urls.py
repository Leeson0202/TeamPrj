from django.urls import path
from info import views

urlpatterns = [
    path('edit_info/', views.edit_info)
]
