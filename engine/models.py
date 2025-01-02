import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class HomepageSliders(models.Model):
    small_text = models.CharField(max_length=128)
    large_text = models.CharField(max_length=128)
    image = models.ImageField(upload_to="homepage/sliders")
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.large_text

    class Meta:
        verbose_name = _("Home Slider")
        verbose_name_plural = _("Homepage Sliders")


class DestinationCategory(models.Model):
    """Optional helper model for categorizing destinations."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = _("Destination Category")
        verbose_name_plural = _("Destination Categories")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Destination(models.Model):
    destination_id = models.UUIDField(_("Destination ID"), default=uuid.uuid4, editable=False, unique=True)
    # Basic Information
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True, help_text="A brief marketing blurb.")
    description = RichTextField(blank=True, help_text="Detailed description of the destination.")

    # Geographic Information
    country = models.CharField(max_length=100, db_index=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True, help_text="Optional full address if applicable.")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, help_text="Latitude for map integration."
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, help_text="Longitude for map integration."
    )

    # Media
    main_image = models.ImageField(upload_to='destinations/main_images/', blank=True, null=True)
    # If you want a gallery, you could create a related model or a JSON field that stores image paths

    # Classification & Tags
    categories = models.ManyToManyField(DestinationCategory, related_name='destinations', blank=True)
    tags = models.CharField(
        max_length=250, blank=True,
        help_text="Comma-separated tags for easier filtering. Example: 'beach, family-friendly'"
    )

    # Ratings & Popularity
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                                         help_text="Average rating based on user reviews.")
    total_reviews = models.PositiveIntegerField(default=0)
    total_trips = models.PositiveIntegerField(default=0, help_text="A computed score for sorting.")

    # Time & Seasonal Information
    best_season = models.CharField(max_length=100, blank=True, help_text="Suggested best time of year to visit.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional External References
    external_id = models.CharField(max_length=100, blank=True, help_text="ID from an external API.")
    website = models.URLField(blank=True)

    # Management fields
    is_active = models.BooleanField(default=True, help_text="Control whether the destination is visible.")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['country']),
        ]
        verbose_name = _("Destination")
        verbose_name_plural = _("Destinations")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.destination.name}"


class Testimonial(models.Model):

    # Basic Author Info
    author_name = models.CharField(
        max_length=100,
        help_text="Name of the person who gave the testimonial."
    )
    author_email = models.EmailField(
        blank=True,
        help_text="Optional email for follow-up. Not displayed publicly."
    )

    # Testimonial Content
    comment = models.TextField(
        help_text="The main content of the testimonial."
    )

    # Optional rating field (1 to 5)
    rating = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Optional rating from 1-5."
    )

    # Display & Moderation
    is_approved = models.BooleanField(
        default=False,
        help_text="Only approved testimonials are displayed publicly."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Highlight this testimonial in featured sections."
    )

    # Tracking
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the testimonial was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the testimonial was last updated."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"Testimonial by {self.author_name} (Approved: {self.is_approved})"


class PackageCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Package Category"
        verbose_name_plural = "Package Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Package(models.Model):
    # Basic Information
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="A concise marketing description."
    )
    description = RichTextField(
        blank=True,
        help_text="Detailed description of the package."
    )

    # Destinations
    # Assumes you have a Destination model already defined
    destinations = models.ManyToManyField(
        'Destination',
        related_name='packages',
        blank=True,
        help_text="Destinations included in this package."
    )

    # Pricing & Currency
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price per person or per package."
    )
    # Pricing & Currency
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price per person or per package."
    )
    currency = models.CharField(
        max_length=10,
        default='USD',
        help_text="Currency code, e.g., USD, EUR."
    )

    # Schedule & Duration
    days = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Duration of the trip in days."
    )
    nights = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Duration of the trip in days."
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="Start date if this is a scheduled departure."
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="End date if this is a scheduled departure."
    )

    # Itinerary & Details
    itinerary = RichTextField(
        blank=True,
        help_text="Detailed day-by-day breakdown of activities."
    )
    included = RichTextField(
        blank=True,
        help_text="List what's included (meals, accommodation, etc.)."
    )
    excluded = models.TextField(
        blank=True,
        help_text="List what's not included (flights, personal expenses, etc.)."
    )

    # Media
    main_image = models.ImageField(
        upload_to='packages/main_images/',
        blank=True,
        null=True
    )

    # Categories & Tags
    categories = models.ManyToManyField(
        PackageCategory,
        related_name='packages',
        blank=True
    )
    tags = models.CharField(
        max_length=250,
        blank=True,
        help_text="Comma-separated tags for filtering (e.g. 'honeymoon, family-friendly')"
    )

    # Ratings & Popularity (if needed)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        help_text="Average rating based on testimonials."
    )
    total_reviews = models.PositiveIntegerField(default=0)

    # Display Controls
    is_active = models.BooleanField(
        default=True,
        help_text="Control if the package is publicly visible."
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Highlight this package in featured sections."
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # External references if needed
    external_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="External reference ID if integrated with another system."
    )
    website = models.URLField(blank=True, help_text="Link to more info or booking page.")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PackageItinerary(models.Model):
    package = models.ForeignKey(Package, related_name='itineraries', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.TextField(null=True)
    description = RichTextField(
        help_text="Detailed day-by-day breakdown of activities."
    )
    image = models.ImageField(upload_to='packages/itineraries')
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Package Itinerary"
        verbose_name_plural = "Package Itineraries"


class PackageImage(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='packages/gallery')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.package.name}"


class Hotel(models.Model):
    destination = models.ForeignKey(Destination, related_name="destination_hotels", null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(DestinationCategory, related_name='hotels', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    main_image = models.ImageField(upload_to='hotels/main_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotels/images/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.hotel.name}"

    class Meta:
        verbose_name = "Hotel Image"
        verbose_name_plural = "Hotel Images"


class Activity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(DestinationCategory, related_name='activities', on_delete=models.CASCADE)
    short_description = models.CharField(max_length=300, blank=True)
    description = RichTextField(blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)  # e.g., "CEO & Founder", "Co-Founder", "Partner"
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)  # Store team member images
    bio = models.TextField(blank=True) # Optional biography
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Our Team"
        ordering = ['name'] # Optional ordering
