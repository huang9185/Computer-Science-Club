from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=Bid)
def bid_change_handler(sender, instance, **kwargs):
    listin = Listing.objects.all().get(prices=instance)
    listin.current_bid = Bid.objects.values("bid").filter(listing=listin).order_by('bid').last()["bid"]
    listin.save()

def categorize(choice):
    # Organize acticve listings into dictionaries
    # Category is key, listing id is value
    # Return a tuple of list and dictionary
    category_li = []
    category_dict = {}

    listings = Listing.objects.all().filter(active=True)

    if choice == "li":
        for listing in listings:
            if listing.category not in category_li:
                category_li.append(listing.category)
        return category_li
    else:
        for listing in listings:
            if listing.category in category_dict:
                category_dict[listing.category].append(listing.pk)
            else:
                category_dict[listing.category] = [listing.pk]

        return category_dict

def checkwatch(username, listing_id):
    # Given user object, listing.id
    # Return boolean value
    user = User.objects.all().get(username=username)
    for item in get_watch(user):
        if item == listing_id:
            return True
    return False


def get_listing(listing_id):
    return Listing.objects.all().get(pk=listing_id)


def get_watch(user):
    # Given user object
    # Return a list of listing.id
    id_list = []
    item_list = Watchitem.objects.all().filter(user=user)
    for item in item_list:
        id_list.append(item.listing_id)
    return id_list

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(active=False),
        "li": categorize("li")
    })

@login_required(login_url="auctions/login.html")
def bid(request, listing_id):
    comments = Comment.objects.all().filter(listing=get_listing(listing_id))
    message = "Your bid must be greater than the current price."
    body = request.POST
    username = request.user.get_username()
    watch = checkwatch(username, listing_id)

    price = int(body["price"])
    listing = get_listing(listing_id)
    if price > listing.starting_bid:
        if price > listing.current_bid:
            new_item = listing.prices.create(
                bid=price,
                owner=username
            )
            listing.current_bid = price
            listing.save()
            message = "Bid Placed Successfully."

    return render(request, "auctions/listing.html", {
        "item": listing,
        "comments": comments,
        "watch": watch,
        "message": message,
        "li": categorize("li")
    })


def category(request, item):
    # Call function to get list of listing.pk under category
    ls = categorize("dict")[item]
    listings = Listing.objects.all().filter(pk__in=ls)

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": item,
        "li": categorize("li")
    })

@login_required(login_url="auctions/login.html")
def close(request, listing_id):
    comments = Comment.objects.all().filter(listing=get_listing(listing_id))
    watch = checkwatch(request.user.get_username(), listing_id)
    listing = get_listing(listing_id)
    winner = listing.prices.order_by('bid').last().owner
    listing.active = False
    listing.winner = winner
    listing.save()
    message = f"Listing Closed. Winner is {winner}."

    return render(request, "auctions/listing.html", {
        "item": listing,
        "comments": comments,
        "watch": watch,
        "message": message,
        "li": categorize("li")
    })

@login_required(login_url="auctions/login.html")
def create(request):
    message = None
    image = None
    category = "No category provided."
    user = request.user
    data = request.POST

    if request.method == "POST":
        if data["category"]:
            category = data["category"]
        if data["image"]:
            image = data["image"]

        new_listing = user.sales.create(
            title=data["title"],
            description=data["description"],
            starting_bid=int(data["starting_bid"]),
            current_bid=int(data["starting_bid"]),
            category=category,
            image_link=image
        )
        return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/create.html")

@login_required(login_url="auctions/login.html")
def feed(request, listing_id):
    comments = Comment.objects.all().filter(listing=get_listing(listing_id))
    watch = checkwatch(request.user.get_username(), listing_id)
    listing = get_listing(listing_id)
    body = request.POST
    comment = Comment(
        listing=listing,
        writer=request.user,
        title=body["title"],
        content=body["content"]
    )
    comment.save()
    message = "Comment created successfully."

    return render(request, "auctions/listing.html", {
        "item": listing,
        "comments": comments,
        "watch": watch,
        "message": message,
        "li": categorize("li")
    })

@login_required(login_url="auctions/login.html")
def edit_watch(request, listing_id):
    comments = Comment.objects.all().filter(listing=get_listing(listing_id))
    behaviour = request.POST["behaviour"]
    username = request.user.get_username()
    watch = checkwatch(username, listing_id)

    # Edit Watchlist
    if behaviour == 'Add to Watchlist':
        message = "Added to watchlist successfully."
        new_item = Watchitem(
            listing_id=listing_id,
            user=User.objects.all().get(username=username)
        )
        new_item.save()
        watch = True
    else:
        message = "Removed from watchlist successfully."
        items = Watchitem.objects.all().filter(listing_id=listing_id)
        for item in items:
            item.delete()
        watch = False

    return HttpResponseRedirect(reverse('watchlist'))

def listings(request, listing_id):
    comments = Comment.objects.all().filter(listing=get_listing(listing_id))
    listing = get_listing(listing_id)

    if comments == None:
        comments = []

    user = request.user
    if not user.is_authenticated:
        return render(request, "auctions/listing.html", {
            "item": listing
        })

    watch = checkwatch(request.user.get_username(), listing_id)
    return render(request, "auctions/listing.html", {
        "item": listing,
        "comments": comments,
        "watch": watch,
        "message": None,
        "li": categorize("li")
    })


def watchlist(request):
    listing_list = []
    user = request.user
    # Each item equals a listing id
    for item in get_watch(user):
        listing_list.append(get_listing(item))
    return render(request, "auctions/watchlist.html", {
        "list": listing_list,
        "li": categorize("li")
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
