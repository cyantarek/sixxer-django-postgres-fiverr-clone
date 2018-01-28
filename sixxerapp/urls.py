from django.urls import path
from . import views

app_name = "sixxer"

urlpatterns = [
    path("", views.home, name="home"),
    path("gigs/<id>/", views.gig_detail, name="gig-detail"),
]