from django.contrib import admin
from .models import Exercise
# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name",)


admin.site.register(Exercise, ExerciseAdmin)