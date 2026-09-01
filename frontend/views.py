from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from accounts.models import User
from teams.models import AthleteProfile
from routines.models import RoutineAssignment, Routine, RoutineExercise
from routines.forms import RoutineForm, RoutineExerciseForm, RoutineAssignmentForm
from results.models import Result, CoachNote
from attendance.models import Attendance
from exercises.forms import ExerciseForm
from exercises.models import Exercise
from django.utils import timezone
from results.forms import CoachNoteForm, ResultForm
from accounts.forms import UserProfileForm
from teams.forms import AthleteProfileForm



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

@login_required
def exercise_management(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.created_by = request.user
            exercise.save()
            return redirect("exercise-management")
    else:
        form = ExerciseForm()

    exercises = Exercise.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "frontend/exercise_management.html", {"form": form, "exercises": exercises})

@login_required
def routine_management(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    if request.method == "POST":
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.created_by = request.user
            routine.save()
            return redirect("routine-management")
    else:
        form = RoutineForm()

    routines = Routine.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "frontend/routine_management.html", {"form": form, "routines": routines})


@login_required
def routine_detail(request, routine_id):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    routine = get_object_or_404(Routine, id=routine_id, created_by=request.user)

    exercise_form = RoutineExerciseForm(
        request.POST if request.method == "POST" and "exercise" in request.POST else None
    )
    assignment_form = RoutineAssignmentForm(
        request.POST if request.method == "POST" and "athlete" in request.POST else None
    )
    # Solo mostrar deportistas de ESTE coach en el selector de asignación
    assignment_form.fields["athlete"].queryset = User.objects.filter(
        athlete_profile__coach=request.user
    )

    if request.method == "POST":
        if "exercise" in request.POST and exercise_form.is_valid():
            re = exercise_form.save(commit=False)
            re.routine = routine
            re.save()
            return redirect("routine-detail", routine_id=routine.id)

        if "athlete" in request.POST and assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.routine = routine
            assignment.assigned_by = request.user
            assignment.save()
            return redirect("routine-detail", routine_id=routine.id)

    context = {
        "routine": routine,
        "exercise_form": exercise_form,
        "assignment_form": assignment_form,
        "routine_exercises": routine.routine_exercises.select_related("exercise"),
        "assignments": routine.assignments.select_related("athlete"),
    }
    return render(request, "frontend/routine_detail.html", context)

@login_required
def attendance_register(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    athletes = AthleteProfile.objects.filter(coach=request.user).select_related("user")
    today = timezone.localdate()

    already_marked = set(
        Attendance.objects.filter(athlete__athlete_profile__coach=request.user, date=today)
        .values_list("athlete_id", flat=True)
    )

    context = {"athletes": athletes, "already_marked": already_marked, "today": today}
    return render(request, "frontend/attendance_register.html", context)

@login_required
def add_note(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    if request.method == "POST":
        form = CoachNoteForm(request.POST)
        form.fields["athlete"].queryset = User.objects.filter(athlete_profile__coach=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.coach = request.user
            note.save()
            return redirect("add-note")
    else:
        form = CoachNoteForm()
        form.fields["athlete"].queryset = User.objects.filter(athlete_profile__coach=request.user)

    notes = CoachNote.objects.filter(coach=request.user).select_related("athlete").order_by("-created_at")[:20]
    return render(request, "frontend/add_note.html", {"form": form, "notes": notes})

@login_required
def register_result(request):
    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.athlete = request.user
            result.save()
            return redirect("register-result")
    else:
        form = ResultForm()

    recent = Result.objects.filter(athlete=request.user).select_related("exercise").order_by("-date")[:10]
    return render(request, "frontend/register_result.html", {"form": form, "recent": recent})


@login_required
def my_results(request):
    exercise_id = request.GET.get("exercise")
    exercises = Exercise.objects.filter(results__athlete=request.user).distinct()

    results = Result.objects.filter(athlete=request.user)
    if exercise_id:
        results = results.filter(exercise_id=exercise_id)
    results = results.order_by("date")

    context = {"exercises": exercises, "results": results, "selected_exercise": exercise_id}
    return render(request, "frontend/my_results.html", context)


@login_required
def mark_attendance(request):
    today = timezone.localdate()
    already_marked = Attendance.objects.filter(athlete=request.user, date=today).exists()

    if request.method == "POST" and not already_marked:
        Attendance.objects.get_or_create(
            athlete=request.user, date=today, defaults={"registered_by": request.user}
        )
        return redirect("mark-attendance")

    context = {"already_marked": already_marked, "today": today}
    return render(request, "frontend/mark_attendance.html", context)


@login_required
def my_notes(request):
    notes = CoachNote.objects.filter(athlete=request.user).select_related("coach").order_by("-created_at")
    return render(request, "frontend/my_notes.html", {"notes": notes})

@login_required
def my_profile(request):
    user_form = UserProfileForm(request.POST or None, instance=request.user)

    athlete_form = None
    if request.user.role == "athlete":
        profile, _ = AthleteProfile.objects.get_or_create(user=request.user)
        athlete_form = AthleteProfileForm(request.POST or None, instance=profile)

    if request.method == "POST":
        user_valid = user_form.is_valid()
        athlete_valid = athlete_form.is_valid() if athlete_form else True

        if user_valid and athlete_valid:
            user_form.save()
            if athlete_form:
                athlete_form.save()
            return redirect("my-profile")

    return render(request, "frontend/my_profile.html", {"user_form": user_form, "athlete_form": athlete_form})

@login_required
def request_coach(request):
    if request.user.role == "coach":
        return redirect("coach-dashboard")

    if request.method == "POST":
        request.user.wants_to_be_coach = True
        request.user.save()
        return redirect("athlete-dashboard")

    return render(request, "frontend/request_coach.html")

@login_required
def mark_attendance_htmx(request, athlete_id):
    if request.user.role != "coach" or request.method != "POST":
        return redirect("athlete-dashboard")

    profile = get_object_or_404(AthleteProfile, user_id=athlete_id, coach=request.user)
    today = timezone.localdate()
    Attendance.objects.get_or_create(
        athlete=profile.user, date=today, defaults={"registered_by": request.user}
    )
    return render(request, "frontend/partials/attendance_row.html", {"athlete": profile, "marked": True})