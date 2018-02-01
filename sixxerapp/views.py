from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.utils.text import slugify

from .models import Gig, Profile
from .forms import GigForm

# Create your views here.

BRAINTREE_MERCHANT = 'your_merchant_key'
BRAINTREE_PUBLIC_KEY = 'your_public_key'
BRAINTREE_PRIVATE_KEY = 'your_private_key'


def home(request):
	gigs = Gig.objects.filter(status=True).order_by("-rating")
	return render(request, "home.html", {"gigs": gigs})

def gig_detail(request, slug):
	gig = Gig.objects.get(slug=slug)
	# client_token = braintree.ClientToken.generate()
	client_token = "AAAA"
	recommends = Gig.objects.filter(status=True)
	return render(request, "gigs/gig_detail.html", {"gig": gig, "recommends": recommends, "client_token": client_token})

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
		gig = Gig.objects.get(request.POST["gig_id"])
		nonce = request.POST["payment_method_nonce"]
		# result = braintree.Transaction.sale({
		# 	"amount": gig.price,
		# 	"payment_method_nonce": nonce
		# })
		#
		# if result.is_success:
		# 	print("Buy Success")
		# else:
		# 	print("Buy Failed")

		return redirect("/")




