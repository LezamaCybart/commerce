from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    description = models.CharField(max_length=100)
    starting_bid = models.FloatField()
    current_price = models.FloatField(null=True, blank=True)

    #optional tag
    tag = models.CharField(max_length=10, null=True, blank=True, default='')

    #optional image
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}: starting bid: {self.starting_bid}, current price {self.current_price}"

    def get_absolute_url(self):
        return reverse('listing-detail', args=(str(self.id)))


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(Auction_listing, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return f"{self.auction_listing.title} {self.name}"


