from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Avg

from accounts.models import User
from teams.models import AthleteProfile, CoachInvitation, AthleteGroup
from routines.models import RoutineAssignment, Routine
from routines.forms import RoutineForm, RoutineExerciseForm, RoutineAssignmentForm, RoutineExercise
from results.models import Result, CoachNote
from attendance.models import Attendance
from exercises.forms import ExerciseForm
from exercises.models import Exercise
from django.utils import timezone
from results.forms import CoachNoteForm, ResultForm
from accounts.forms import UserProfileForm
from teams.forms import AthleteProfileForm
from datetime import timedelta
import json



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
def group_list(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            AthleteGroup.objects.create(coach=request.user, name=name)
        return redirect("group-list")

    groups = AthleteGroup.objects.filter(coach=request.user).prefetch_related("athletes__user")
    return render(request, "frontend/group_list.html", {"groups": groups})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(AthleteGroup, id=group_id, coach=request.user)

    if request.method == "POST":
        athlete_id = request.POST.get("athlete_id")
        action = request.POST.get("action")
        # Solo deja tocar deportistas que son del Coach dueño del grupo
        profile = get_object_or_404(AthleteProfile, id=athlete_id, coach=request.user)

        if action == "add":
            group.athletes.add(profile)
        elif action == "remove":
            group.athletes.remove(profile)

        return redirect("group-detail", group_id=group.id)

    members = group.athletes.select_related("user")
    available = AthleteProfile.objects.filter(coach=request.user).exclude(id__in=members).select_related("user")
    return render(request, "frontend/group_detail.html", {
        "group": group,
        "members": members,
        "available": available,
    })


@login_required
def athlete_dashboard(request):
    # El banner de "pendiente de aprobación como Entrenador" se muestra acá mismo
    assignments = RoutineAssignment.objects.filter(athlete=request.user).select_related("routine")
    pending_invitations = CoachInvitation.objects.filter(
        athlete=request.user, status=CoachInvitation.Status.PENDING
    ).select_related("coach")
    return render(request, "frontend/athlete_dashboard.html", {
        "assignments": assignments,
        "pending_invitations": pending_invitations,
    })
    
@login_required
def my_routine_detail(request, routine_id):
    if request.user.role != "athlete":
        return redirect("coach-dashboard")

    assignment = get_object_or_404(
        RoutineAssignment.objects.select_related("routine"),
        routine_id=routine_id, athlete=request.user
    )
    routine_exercises = assignment.routine.routine_exercises.select_related("exercise")
    return render(request, "frontend/my_routine_detail.html", {
        "routine": assignment.routine,
        "routine_exercises": routine_exercises,
    })

@login_required
def my_groups(request):
    if request.user.role != "athlete":
        return redirect("coach-dashboard")

    profile, _ = AthleteProfile.objects.get_or_create(user=request.user)
    groups = profile.groups.select_related("coach")
    return render(request, "frontend/my_groups.html", {"groups": groups})

@login_required
def leave_group(request, group_id):
    profile, _ = AthleteProfile.objects.get_or_create(user=request.user)
    group = get_object_or_404(AthleteGroup, id=group_id, athletes=profile)

    if request.method == "POST":
        group.athletes.remove(profile)
        return redirect("my-groups")

    return render(request, "frontend/leave_group_confirm.html", {"group": group})

@login_required
def athlete_detail(request, athlete_id):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    profile = get_object_or_404(AthleteProfile, user_id=athlete_id, coach=request.user)

    all_results = Result.objects.filter(athlete_id=athlete_id).select_related("exercise").order_by("date")

    # Agrupar resultados por ejercicio para el selector del gráfico
    results_by_exercise = {}
    for r in all_results:
        key = str(r.exercise_id)
        if key not in results_by_exercise:
            results_by_exercise[key] = {"name": r.exercise.name, "dates": [], "weights": []}
        results_by_exercise[key]["dates"].append(r.date.strftime("%d/%m"))
        results_by_exercise[key]["weights"].append(float(r.weight_kg) if r.weight_kg is not None else None)

    context = {
        "profile": profile,
        "results": all_results.order_by("-date")[:20],
        "results_by_exercise_json": json.dumps(results_by_exercise),
        "notes": CoachNote.objects.filter(athlete_id=athlete_id).order_by("-created_at")[:10],
        "attendances": Attendance.objects.filter(athlete_id=athlete_id).order_by("-date")[:10],
        "assignments": RoutineAssignment.objects.filter(athlete_id=athlete_id).select_related("routine"),
    }
    return render(request, "frontend/athlete_detail.html", context)

@login_required
def exercise_management(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")
    return render(request, "frontend/exercise_management.html")


@login_required
def exercise_list(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")
    exercises = Exercise.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "frontend/exercise_list.html", {"exercises": exercises})


@login_required
def exercise_create(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.created_by = request.user
            exercise.save()
            return redirect("exercise-list")
    else:
        form = ExerciseForm()

        return render(request, "frontend/exercise_create.html", {"form": form})

@login_required
def exercise_edit(request, exercise_id):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    exercise = get_object_or_404(Exercise, id=exercise_id, created_by=request.user)

    if request.method == "POST":
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect("exercise-list")
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, "frontend/exercise_edit.html", {"form": form, "exercise": exercise})

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
    # Solo mostrar ejercicios creados por ESTE coach en el selector
    exercise_form.fields["exercise"].queryset = Exercise.objects.filter(created_by=request.user)
    
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
            last = routine.routine_exercises.order_by("-order").first()
            re.order = (last.order if last else 0) + 1
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
def remove_routine_exercise(request, re_id):
    if request.method != "POST":
        return redirect("coach-dashboard")

    routine_exercise = get_object_or_404(
        RoutineExercise, id=re_id, routine__created_by=request.user
    )
    routine_id = routine_exercise.routine_id
    routine_exercise.delete()
    return redirect("routine-detail", routine_id=routine_id)

@login_required
def move_routine_exercise(request, re_id, direction):
    if request.method != "POST":
        return redirect("coach-dashboard")

    routine_exercise = get_object_or_404(
        RoutineExercise, id=re_id, routine__created_by=request.user
    )
    siblings = list(routine_exercise.routine.routine_exercises.order_by("order"))
    index = siblings.index(routine_exercise)

    other = None
    if direction == "up" and index > 0:
        other = siblings[index - 1]
    elif direction == "down" and index < len(siblings) - 1:
        other = siblings[index + 1]

    if other:
        routine_exercise.order, other.order = other.order, routine_exercise.order
        routine_exercise.save()
        other.save()

    return redirect("routine-detail", routine_id=routine_exercise.routine_id)

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

@login_required
def invite_athlete(request):
    if request.user.role != "coach":
        return redirect("athlete-dashboard")

    sent = False
    error = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        athlete = User.objects.filter(email__iexact=email, role="athlete").first()
        if athlete:
            CoachInvitation.objects.create(coach=request.user, athlete=athlete)
            sent = True
        else:
            error = "No hay ningún Deportista registrado con ese email."

    return render(request, "frontend/invite_athlete.html", {"sent": sent, "error": error})

@login_required
def respond_invitation(request, invitation_id):
    if request.method != "POST":
        return redirect("athlete-dashboard")

    invitation = get_object_or_404(
        CoachInvitation, id=invitation_id, athlete=request.user, status=CoachInvitation.Status.PENDING
    )
    action = request.POST.get("action")

    if action == "accept":
        invitation.status = CoachInvitation.Status.ACCEPTED
        invitation.save()
        profile = request.user.athlete_profile
        profile.coach = invitation.coach
        profile.save()
    elif action == "reject":
        invitation.status = CoachInvitation.Status.REJECTED
        invitation.save()

    return redirect("athlete-dashboard")