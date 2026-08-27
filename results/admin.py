from django.contrib import admin
from .models import Result, CoachNote
# Register your models here.

class ResultAdmin(admin.ModelAdmin):
    list_display = ("athlete", "exercise", "date", "reps", "weight_kg", "duration_seconds", "distance_m")
    list_filter = ("exercise", "date")
    search_fields = ("athlete__username", "athlete__first_name", "athlete__last_name")


class CoachNoteAdmin(admin.ModelAdmin):
    list_display = ("athlete", "coach", "created_at")
    search_fields = ("athlete__username",)


admin.site.register(Result, ResultAdmin)
admin.site.register(CoachNote, CoachNoteAdmin)