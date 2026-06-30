from django.urls import path
from .views import *
urlpatterns=[
    path('',CartView.as_view()),
    path('cartitem/<int:id>/',CartItemView.as_view()),
]