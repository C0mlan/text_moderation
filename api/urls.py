from django.urls import path
from . import views

urlpatterns =[
    path('register/', views.register_view, name = 'register'),
    path('test/', views.test_view, name = 'test'),
    path('text_predict/', views.text_predict, name='text_predict'),

    
]