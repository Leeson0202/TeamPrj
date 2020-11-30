from django.urls import path
from remember import views

urlpatterns = [
    path('select/', views.select),
    path('add/', views.add),
    path('false/', views.false),
    path('get_word/', views.get_word),
    path('get_word_id/', views.get_word_id),
]
