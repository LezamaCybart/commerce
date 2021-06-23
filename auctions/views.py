from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required

from .models import User, Auction_listing, Watchlist


"""
def index(request):
    return render(request, "auctions/index.html", { 
        "listings": Auction_listing.objects.all()
        })
"""
class Index(ListView):
    model = Auction_listing
    template_name = 'auctions/index.html'

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

class Listing(DetailView):
    model = Auction_listing
    template_name = 'auctions/listing.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['watchlist'] = Watchlist.objects.get(author=self.request.user)
            context['usuario'] = self.request.user
            return context

class New_Listing(LoginRequiredMixin, CreateView):
    model = Auction_listing
    template_name = 'auctions/new-listing.html'
    fields = ('title', 'description', 'starting_bid', 'tag', 'image')

    def form_valid(self, form):
        form.instance.current_price = form.instance.starting_bid
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login')
def add_to_watchlist(request, listing_key):
    listing = Auction_listing.objects.get(pk = listing_key)

    if request.method == "POST":
        watchlist, created = Watchlist.objects.get_or_create(author = request.user)
        watchlist.auction_listing.add(listing)
        return redirect('listing-detail', pk=listing_key)

@login_required(login_url='/login')
def remove_from_watchlist(request, listing_key):
    listing = Auction_listing.objects.get(pk = listing_key)

    if request.method == "POST":
        watchlist, created = Watchlist.objects.get_or_create(author = request.user)
        watchlist.auction_listing.remove(listing)
        return redirect('listing-detail', pk=listing_key)
    


