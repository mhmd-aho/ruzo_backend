from django.urls import path
from .views import *
urlpatterns=[
    path('',OrderView.as_view()),
    path('<int:id>/',OrderView.as_view()),
    path('checkout/',CheckOutView.as_view()),
]