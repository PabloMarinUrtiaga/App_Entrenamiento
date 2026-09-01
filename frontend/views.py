from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import User
from teams.models import AthleteProfile
from routines.models import RoutineAssignment
from results.models import Result, CoachNote
from attendance.models import Attendance


# Create your views here.

def landing(request):
    # Si ya está logueado, lo mandamos directo a su dashboard según el rol
    if request.user.is_authenticated:
        if request.user.role == "coach":
            return redirect("coach-dashboard")
        return redirect("athlete-dashboard")
    return render(request, "frontend/landing.html")

@login_required
def coach_dashboard(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    athletes = AthleteProfile.objects.filter(coach=request.user).select_related("user")
    return render(request, "frontend/coach_dashboard.html", {"athletes": athletes})


@login_required
def athlete_dashboard(request):
    # El banner de "pendiente de aprobación como Entrenador" se muestra acá mismo
    assignments = RoutineAssignment.objects.filter(athlete=request.user).select_related("routine")
    return render(request, "frontend/athlete_dashboard.html", {"assignments": assignments})

@login_required
def athlete_detail(request, athlete_id):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    # get_object_or_404 con coach=request.user: si el deportista no es SUYO, devuelve 404, no 403
    profile = get_object_or_404(AthleteProfile, user_id=athlete_id, coach=request.user)

    context = {
        "profile": profile,
        "results": Result.objects.filter(athlete_id=athlete_id).select_related("exercise")[:20],
        "notes": CoachNote.objects.filter(athlete_id=athlete_id).order_by("-created_at")[:10],
        "attendances": Attendance.objects.filter(athlete_id=athlete_id).order_by("-date")[:10],
        "assignments": RoutineAssignment.objects.filter(athlete_id=athlete_id).select_related("routine"),
    }
    return render(request, "frontend/athlete_detail.html", context)