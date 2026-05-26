from django.urls import path
from .views import *
urlpatterns=[
    path('order/',OrderView.as_view()),
    path('order/<int:id>/',OrderView.as_view()),
    path('checkout/',CheckOutView.as_view()),
]