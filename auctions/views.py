from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import User, Auction_listing


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

class New_Listing(LoginRequiredMixin, CreateView):
    model = Auction_listing
    template_name = 'auctions/new-listing.html'
    fields = ('title', 'description', 'starting_bid', 'tag', 'image')

    def form_valid(self, form):
        form.instance.current_price = form.instance.starting_bid
        form.instance.author = self.request.user
        return super().form_valid(form)

