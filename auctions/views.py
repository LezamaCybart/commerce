from django.contrib.auth import authenticate, login, logout, models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages

from .models import User, Auction_listing, Watchlist, Bid

class BidForm(forms.Form):
    amount = forms.FloatField(label="amount to bid")

class Index(ListView):
    model = Auction_listing
    template_name = 'auctions/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_prices_list'] = get_current_prices_list()
        return context

def get_current_prices_list():
    current_prices_list = list()

    listings = Auction_listing.objects.all()

    for listing in listings:
        bids = Bid.objects.filter(listing_id=listing.pk)
        if len(bids) == 0:
            current_price = listing.starting_bid
        else:
            current_price = bids.order_by('-amount')[0].amount
        current_prices_list.append(current_price)

    return current_prices_list



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
            context['watchlist'] = Watchlist.objects.get_or_create(author=self.request.user)
            context['usuario'] = self.request.user
            context['bid_form'] = BidForm
            bids = Bid.objects.filter(listing_id=self.object.pk)
            if len(bids) == 0:
                context['current_price'] = Auction_listing.objects.get(pk=self.object.pk).starting_bid
            else:
                context['current_price'] = bids.order_by('-amount')[0].amount
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
    watchlist, created = Watchlist.objects.get_or_create(author = request.user)

    if request.method == "POST":
        listing = Auction_listing.objects.get(pk = listing_key)
        watchlist.auction_listing.add(listing)
        return redirect('listing-detail', pk=listing_key)

@login_required(login_url='/login')
def remove_from_watchlist(request, listing_key):
    watchlist, created = Watchlist.objects.get_or_create(author = request.user)

    if request.method == "POST":
        listing = Auction_listing.objects.get(pk = listing_key)
        watchlist.auction_listing.remove(listing)
        return redirect('listing-detail', pk=listing_key)
    

"""
class Create_Bid(LoginRequiredMixin, CreateView):
    model = Bid
    template_name = 'auctions/new-bid.html'
    fields = ('amount')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
"""

@login_required(login_url='/login')
def bid(request, listing_key):
    form = BidForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data["amount"]

    bids = Bid.objects.filter(listing_id=listing_key)

    if len(bids) == 0:
        current_price = Auction_listing.objects.get(pk=listing_key).starting_bid
    else:
        current_price = bids.order_by('-amount')[0].amount

    if amount > current_price:
        bin = Bid(user=request.user, listing=Auction_listing.objects.get(pk=listing_key), amount=amount)
        bin.save()
        return redirect('listing-detail', pk=listing_key)
    else:
        messages.add_message(request, messages.WARNING, "Go higher!")
        return redirect('listing-detail', pk=listing_key)

@login_required(login_url='/login')
def close_listing(request, listing_key):
    if request.method == "POST":
        bids = Bid.objects.filter(listing_id=listing_key)

        listing = Auction_listing.objects.get(pk=listing_key)

        listing.is_active = False
        listing.save()

        if len(bids) != 0:
            winner = bids.order_by('-amount')[0].user
            listing.winner = winner
            listing.save()
            return redirect('listing-detail', pk=listing_key)

        return redirect('listing-detail', pk=listing_key)
