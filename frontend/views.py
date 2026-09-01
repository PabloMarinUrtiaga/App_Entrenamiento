from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from teams.models import AthleteProfile
from routines.models import RoutineAssignment


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