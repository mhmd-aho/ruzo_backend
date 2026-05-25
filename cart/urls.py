from django.urls import path
from .views import *
urlpatterns=[
    path('cart/',CartView.as_view()),
    path('cartitem/delete/<int:id>/',CartItemDeleteView.as_view()),
    path('cartitem/update/<int:id>/',CartItemUpdateView.as_view()),
]