from Buyer import views
from django.urls import path
urlpatterns = [ 
    path("new_order/", views.new_order), 
    path("payment/", views.payment),
    path("add_funds/", views.add_funds),
]