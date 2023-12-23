from Seller import views
from django.urls import path
urlpatterns = [ 
    path("create_store/", views.create_store), 
    path("add_book/", views.add_book),
    path("add_stock_level/", views.add_stock_level),
]