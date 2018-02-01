from django.urls import path
from . import views

app_name = "sixxer"

urlpatterns = [
    path("", views.home, name="home"),
	path("mygigs/", views.my_gigs, name="my-gigs"),
	path("buyings/", views.my_buyings, name="my-buyings"),
	path("sellings/", views.my_sellings, name="my-sellings"),
	path("creategig/", views.create_gig, name="gig-create"),
    path("<slug>/editgig/", views.edit_gig, name="gig-edit"),
    path("gigs/<slug>/", views.gig_detail, name="gig-detail"),
    path("profile/<str:username>", views.my_profile, name="my-profile"),
    path("purchase/", views.create_purchase, name="create-purchase"),
    path("add_review/", views.add_review, name="add-review"),
    path("search/", views.search, name="search"),
    path("category/", views.categories, name="category"),
]