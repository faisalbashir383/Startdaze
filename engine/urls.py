from django.urls import path
from engine.views import Homepage, ContactPage, AboutPage, PrivacyPage, DestinationDetailView, HotelDetailView

urlpatterns = [
    path("", Homepage, name="homepage"),
    path("contact/", ContactPage, name="contactpage"),
    path("about/", AboutPage, name="aboutPage"),
    path("privacy/", PrivacyPage, name="PrivacyPage"),
    path("destination/<str:slug>/", DestinationDetailView, name="DestinationDetailView"),
    path("hotel/<str:slug>/", HotelDetailView, name="hotel_detail"),
]
