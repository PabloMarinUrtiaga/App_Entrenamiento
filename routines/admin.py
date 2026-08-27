from django.contrib import admin
from .models import Routine, RoutineExercise, RoutineAssignment
# Register your models here.

class RoutineExerciseInline(admin.TabularInline):
    model = RoutineExercise
    extra = 1


class RoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    inlines = [RoutineExerciseInline]


class RoutineAssignmentAdmin(admin.ModelAdmin):
    list_display = ("routine", "athlete", "assigned_by", "updated_at")
    list_filter = ("routine",)


admin.site.register(Routine, RoutineAdmin)
admin.site.register(RoutineAssignment, RoutineAssignmentAdmin)