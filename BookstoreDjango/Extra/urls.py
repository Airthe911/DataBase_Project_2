from Extra import views
from django.urls import path
urlpatterns = [ 
    path("delivery/", views.delivery), 
    path("receipt/", views.receipt),
    path("lookup/", views.lookup),
    path("cancer/", views.cancer),
]