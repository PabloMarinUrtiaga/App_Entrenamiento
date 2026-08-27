from django.contrib import admin
from .models import Attendance

# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("athlete", "date", "registered_by")
    list_filter = ("date",)
    search_fields = ("athlete__username",)


admin.site.register(Attendance, AttendanceAdmin)

