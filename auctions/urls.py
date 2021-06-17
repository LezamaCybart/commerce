from django.urls import path

from . import views
from .views import Index, Listing, New_Listing

urlpatterns = [
    #path("", views.index, name="index"), using class based urls instead
    path('', Index.as_view(), name="index"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("listing/<int:pk>", Listing.as_view(), name="listing-detail"),
    path("new_listing/", New_Listing.as_view(), name="new_listing")
]
