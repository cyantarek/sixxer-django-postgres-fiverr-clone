from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Gig, Profile
from .forms import GigForm

# Create your views here.

def home(request):
	gigs = Gig.objects.filter(status=True)
	return render(request, "home.html", {"gigs": gigs})

def gig_detail(request, id):
	print("Called")
	gig = Gig.objects.get(id=id)
	return render(request, "gigs/gig_detail.html", {"gig": gig})

@login_required(login_url="/")
def create_gig(request):
	error = None
	if request.method == "POST":
		gig_form = GigForm(request.POST, request.FILES)
		if gig_form.is_valid():
			gig = gig_form.save(commit=False)
			gig.user = request.user
			gig.save()
			return redirect("/mygigs/")
		else:
			error = gig_form.errors
	gig_form = GigForm()
	return render(request, "gigs/create_gig.html", {"gig_form": gig_form, "error": error})

@login_required(login_url="/")
def edit_gig(request, id):
	error = None
	gig = Gig.objects.get(id=id, user=request.user)
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
	gigs = Gig.objects.filter(user=profile.user, status=True)

	return render(request, "profile.html", {"profile": profile, "gigs": gigs})









