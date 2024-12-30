from django.http import HttpResponse
from django.shortcuts import render

from engine.models import DestinationCategory, HomepageSliders, Destination, Activity, TeamMember


def Homepage(request):
    # Prefetch related hotels, images, and activities to optimize queries
    categories = DestinationCategory.objects.prefetch_related(
        'destinations',
        'hotels',
        'activities'
    )
    return render(request, 'index.html', context={
        "destinations_categories": categories,
        "sliders": HomepageSliders.objects.filter(is_active=True),
        "top_destinations": Destination.objects.filter(is_active=True).order_by('-total_trips')[:6],
        "activities": Activity.objects.all()
    })


def ContactPage(request):
    return render(request, 'contact.html')


def AboutPage(request):
    context = {
        "team_members": TeamMember.objects.filter(is_active=True)
    }
    return render(request, 'about.html', context=context)


def PrivacyPage(request):
    return render(request, 'privacy.html')


def DestinationDetailView(request, slug):
    try:
        destination = Destination.objects.get(slug=slug)
        return render(request, 'destination_detail.html', context={
            "destination": destination
        })
    except Exception as e:
        return HttpResponse(str(e))


def HotelDetailView(request, slug):
    return HttpResponse("Page Not Available please try after few days")
