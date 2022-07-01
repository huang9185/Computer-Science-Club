from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=64, blank=False)
    starting_bid = models.IntegerField(blank=False)
    current_bid = models.IntegerField(blank=False, default=0)
    category = models.CharField(max_length=64, blank=True)
    image_link = models.CharField(max_length=100, null=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(blank=False, default=True)
    winner = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.title}: {self.description} with starting bid at {self.starting_bid}"

class Bid(models.Model):
    owner = models.CharField(max_length=64, default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="prices")
    bid = models.IntegerField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.listing}: {self.bid}"

class Watchitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing_id = models.IntegerField(blank=False)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)

class Comment(models.Model):
    writer = models.CharField(max_length=64)
    title = models.CharField(max_length=64, blank=False)
    content = models.TextField(blank=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="feedback")
    time = models.DateTimeField(auto_now=False, auto_now_add=True)