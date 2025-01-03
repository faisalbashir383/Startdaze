from django.http import HttpResponse
from django.shortcuts import render

from engine.models import DestinationCategory, HomepageSliders, Destination, Activity, TeamMember, Package


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
        "activities": Activity.objects.all(),
        "packages": Package.objects.all()
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
        related_destinations = Destination.objects.filter(
            categories__in=destination.categories.all()
        ).exclude(id=destination.id).distinct()
        return render(request, 'destination_detail.html', context={
            "destination": destination,
            "related_destinations": related_destinations
        })
    except Exception as e:
        return HttpResponse(str(e))


def HotelDetailView(request, slug):
    return HttpResponse("Page Not Available please try after few days")


def PackageDetailView(request, slug):
    try:
        package = Package.objects.get(slug=slug)
        return render(
            request, "package_detail_view.html",
            context={
                "package": package
            }
        )
    except Exception as e:
        return HttpResponse(str(e))