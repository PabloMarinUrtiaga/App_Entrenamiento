from django.contrib import admin
from .models import AthleteProfile

# Register your models here.


class AthleteProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "coach", "position", "sub_position", "weight_kg", "height_cm")
    list_filter = ("position", "coach")
    search_fields = ("user__username", "user__first_name", "user__last_name")


admin.site.register(AthleteProfile, AthleteProfileAdmin)
