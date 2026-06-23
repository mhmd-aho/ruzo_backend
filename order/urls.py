from django.urls import path
from .views import *
urlpatterns=[
    path('checkout/',CheckOutView.as_view()),
    path('',OrdersView.as_view()),
    path('<int:id>/',OrderView.as_view()),
]