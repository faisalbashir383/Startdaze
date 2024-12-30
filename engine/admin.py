from django.contrib import admin
from engine.models import HomepageSliders, DestinationCategory, Destination, Hotel, TeamMember


class HomepageSlidersAdmin(admin.ModelAdmin):
    list_display = ("small_text", "large_text", "is_active", "added_on", "updated_on")
    list_filter = ("is_active", "added_on")
    search_fields = ("small_text", "large_text")


class DestinationCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        "name", "is_active", "country", "city", "region", "average_rating", "total_reviews",
        "best_season", "created_at", "updated_at"
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description", "categories")


class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "name", "slug", "category", "rating", "is_active"
    )
    list_filter = ("is_active", "category")
    search_fields = ("name",)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name", "title", "is_active", "created_at"
    )


admin.site.register(HomepageSliders, HomepageSlidersAdmin)
admin.site.register(DestinationCategory, DestinationCategoryAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
