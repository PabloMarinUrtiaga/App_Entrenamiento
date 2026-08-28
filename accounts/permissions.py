from rest_framework import permissions

class IsApproved(permissions.BasePermission):
    # Bloquea a cualquier usuario que todavía no fue aprobado, sin importar el rol
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_approved)


class IsCoach(permissions.BasePermission):
    # Permite la acción solo si el usuario logueado tiene rol Entrenador y está aprobado
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_approved
            and request.user.role == "coach"
        )


class IsCoachOrReadOnly(permissions.BasePermission):
    # Cualquier usuario aprobado puede leer (GET). Solo el Coach puede crear/editar/borrar.
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and request.user.is_approved):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == "coach"


class IsCoachOfAthleteOrSelf(permissions.BasePermission):
    """
    Para objetos ligados a un deportista puntual (Result, Attendance, CoachNote, RoutineAssignment):
    - El Entrenador puede operar si es el coach asignado a ese deportista.
    - El Deportista puede operar solo sobre sus propios datos.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_approved:
            return False

        athlete = obj.athlete

        if user.role == "athlete":
            return athlete == user

        if user.role == "coach":
            return hasattr(athlete, "athlete_profile") and athlete.athlete_profile.coach == user

        return False