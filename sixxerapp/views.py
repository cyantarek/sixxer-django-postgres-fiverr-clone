from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.text import slugify

from .models import Gig, Profile, Purchase, Review
from .forms import GigForm

# Create your views here.

BRAINTREE_MERCHANT = 'your_merchant_key'
BRAINTREE_PUBLIC_KEY = 'your_public_key'
BRAINTREE_PRIVATE_KEY = 'your_private_key'


category = {
		"graphics-design": "GD",
		"digital-marketing": "DM",
		"web-development": "WD",
		"programming-tech": "PT",
		"video-animation": "VA",
	}

def home(request):
	gigs = Gig.objects.filter(status=True).order_by("-rating")

	return render(request, "home.html", {"gigs": gigs})

def search(request):
	gigs = Gig.objects.filter(title__contains=request.GET["s"])
	return render(request, "home.html", {"gigs": gigs})

def categories(request):
	gigs = Gig.objects.filter(category__exact=category[request.GET["c"]])
	return render(request, "home.html", {"gigs": gigs})

def gig_detail(request, slug):
	gig = Gig.objects.get(slug=slug)
	bought = False
	reviewed = False
	orders = gig.purchase_set.count()
	if not request.user.is_anonymous:
		if gig.purchase_set.filter(buyer=request.user):
			bought = True
		if gig.review_set.filter(user=request.user):
			reviewed = True
	reviews = Review.objects.filter(gig=gig)
	recommends = Gig.objects.filter(status=True)
	return render(request, "gigs/gig_detail.html", {"gig": gig, "recommends": recommends, "reviews": reviews, "bought": bought, "reviewed": reviewed, "orders": orders})

@login_required(login_url="/")
def create_gig(request):
	error = None
	if request.method == "POST":
		gig_form = GigForm(request.POST, request.FILES)
		if gig_form.is_valid():
			gig = gig_form.save(commit=False)
			gig.user = request.user
			gig.slug = slugify(gig_form.cleaned_data.get("title"))
			gig.save()
			return redirect("/mygigs/")
		else:
			error = gig_form.errors
	gig_form = GigForm()
	return render(request, "gigs/create_gig.html", {"gig_form": gig_form, "error": error})

@login_required(login_url="/")
def edit_gig(request, slug):
	error = None
	gig = Gig.objects.get(slug=slug, user=request.user)
	if request.method == "POST":
		gig_form = GigForm(request.POST, request.FILES, instance=gig)
		if gig_form.is_valid():
			gig.save()
			return redirect("/mygigs/")
		else:
			error = gig_form.errors
	return render(request, "gigs/edit_gig.html", {"gig": gig, "error": error})

@login_required(login_url="/")
def my_gigs(request):
	gigs = Gig.objects.filter(user=request.user)
	return render(request, "gigs/my_gigs.html", {"gigs": gigs})

@login_required(login_url="/")
def my_buyings(request):
	purchases = Purchase.objects.filter(buyer=request.user)
	return render(request, "gigs/my_buyings.html", {"purchases": purchases})

@login_required(login_url="/")
def my_sellings(request):
	sellings = Purchase.objects.filter(gig__user=request.user)
	return render(request, "gigs/my_sellings.html", {"sellings": sellings})

def my_profile(request, username):
	profile = Profile.objects.get(user__username=username)
	if request.user == profile.user:
		gigs = Gig.objects.filter(user=profile.user)
	else:
		gigs = Gig.objects.filter(user=profile.user, status=True)

	return render(request, "profile_2.html", {"profile": profile, "gigs": gigs})


@login_required(login_url="/")
def create_purchase(request):
	if request.method == "POST":
		gig = Gig.objects.get(id=request.POST["gig_id"])
		Purchase.objects.create(gig=gig, buyer=request.user)
		return redirect("/buyings/")

@login_required(login_url="/")
def add_review(request):
	gig = Gig.objects.get(id=request.POST["gig_id"])
	Review.objects.create(gig=gig, user=request.user, content=request.POST["content"])
	return redirect(request.META.get("HTTP_REFERER"))
