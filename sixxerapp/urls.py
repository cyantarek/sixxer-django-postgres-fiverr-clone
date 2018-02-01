from django.urls import path
from . import views

app_name = "sixxer"

urlpatterns = [
    path("", views.home, name="home"),
	path("mygigs/", views.my_gigs, name="my-gigs"),
	path("creategig/", views.create_gig, name="gig-create"),
    path("<int:id>/editgig/", views.edit_gig, name="gig-edit"),
    path("gigs/<int:id>/", views.gig_detail, name="gig-detail"),
    path("profile/<str:username>", views.my_profile, name="my-profile"),
    path("checkout/", views.create_purchase, name="create-purchase"),
]