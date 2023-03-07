from django.urls import path
from .views import RestaurantList, RestaurantDetail, MenuList, MenuDetail, MenuItemList, MenuItemDetail

urlpatterns = [
    path('restaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),
    path('menus/', MenuList.as_view(), name='menu-list'),
    path('menus/<int:pk>/', MenuDetail.as_view(), name='menu-detail'),
    path('menu-items/', MenuItemList.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),
]
