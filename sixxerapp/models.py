from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Count


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.CharField(max_length=500)
	about = models.CharField(max_length=1000)
	slogan = models.CharField(max_length=500, default="My Slogan")

	def __str__(self):
		return self.user.username


class Gig(models.Model):
	CATEGORY_CHOICES = (
		("GD", "Graphics & Design"),
		("DM", "Digital Marketing"),
		("WD", "Web Development"),
		("PT", "Programming & Tech"),
		("VA", "Video & Animation"),
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE)

	title = models.CharField(max_length=500)
	category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
	description = models.CharField(max_length=1000)
	price = models.IntegerField(default=6)
	photo = models.FileField(upload_to="gigs")
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.title

PURCHASE_CHOICES = (
	("1", "In Progress"),
	("2", "Completed"),
	("3", "Cancelled"),
	("4", "Incomplete"),
)

class Purchase(models.Model):
	gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	status = models.CharField(choices=PURCHASE_CHOICES, max_length=1, default=1)

	def __str__(self):
		return self.gig.title


class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
	content = models.CharField(max_length=500)

	def __str__(self):
		return self.content















