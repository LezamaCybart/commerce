from django.urls import path

from . import views
from .views import Index, Listing, New_Listing, WatchlistView, category_list

urlpatterns = [
    #path("", views.index, name="index"), using class based urls instead
    path('', Index.as_view(), name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_to_watchlist/<int:listing_key>", views.add_to_watchlist, name="add_watchlist"),
    path("remove_from_watchlist/<int:listing_key>", views.remove_from_watchlist, name="remove_watchlist"),
    path("bid/<int:listing_key>", views.bid, name="bid"),
    path("close_listing/<int:listing_key>", views.close_listing, name="close_auction"),
    path("comment/<int:listing_key>", views.comment, name="comment"),
    path("categories", views.categories_list, name="categories-list"),
    path("category/<str:category>", views.category_list, name="category-list"),

    path("listing/<int:pk>", Listing.as_view(), name="listing-detail"),
    path("new_listing/", New_Listing.as_view(), name="new_listing"),
    path("watchlist/<int:pk>", WatchlistView.as_view(), name="watchlist")
]
