from django.urls import path
from .views import *
urlpatterns=[
    path('',ProductsListView.as_view()),
    path('create/',ProductCreateView.as_view()),
    path('<int:id>/',ProductRetrieveView.as_view()),
    path('<int:id>/update',ProductModifyView.as_view()),
    path('<int:product_id>/variants/',ProductVariantListView.as_view()),
    path('categories/',CategoryListView.as_view()),
    path('categories/create/',CategoryCreateView.as_view()),
    path('categories/<int:id>/update',CategoryModifyView.as_view()),
    path('colors/',ColorListView.as_view()),
    path('colors/create/',ColorCreateView.as_view()),
    path('colors/<int:id>/',ColorModifyView.as_view()),
    path('sizes/',SizeListView.as_view()),
    path('sizes/create/',SizeCreateView.as_view()),
    path('sizes/<int:id>/',SizeModifyView.as_view()),
    path('media/',MediaListView.as_view()),
    path('media/create/',MediaCreateView.as_view()),
    path('<int:product_variant_id>/media/',ProductMediaListView.as_view()),
    path('media/<int:id>/',MediaModifyView.as_view()),
]
