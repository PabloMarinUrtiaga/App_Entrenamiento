from django.contrib import admin
from .models import AthleteProfile, CoachInvitation

# Register your models here.


class AthleteProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "coach", "position", "sub_position", "weight_kg", "height_cm")
    list_filter = ("position", "coach")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    
class CoachInvitationAdmin(admin.ModelAdmin):
    list_display = ("coach", "athlete", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("coach__username", "athlete__username", "athlete__email")


admin.site.register(AthleteProfile, AthleteProfileAdmin)
admin.site.register(CoachInvitation, CoachInvitationAdmin)
