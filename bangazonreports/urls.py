from django.urls import path
from .views import user_fav_seller_list

urlpatterns = [
    path('reports/favoritesellers', user_fav_seller_list),
]
