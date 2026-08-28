from rest_framework import permissions


class IsCoach(permissions.BasePermission):
    # Permite la acción solo si el usuario logueado tiene rol Entrenador y está aprobado
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_approved
            and request.user.role == "coach"
        )


class IsApproved(permissions.BasePermission):
    # Bloquea a cualquier usuario que todavía no fue aprobado, sin importar el rol
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_approved


class IsCoachOfAthleteOrSelf(permissions.BasePermission):
    """
    Para objetos ligados a un deportista puntual (Result, Attendance, CoachNote, etc.):
    - El Entrenador puede operar si es el coach asignado a ese deportista.
    - El Deportista puede operar solo sobre sus propios datos.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_approved:
            return False

        athlete = obj.athlete  # asume que el modelo tiene un campo `athlete`

        if user.role == "athlete":
            return athlete == user

        if user.role == "coach":
            return hasattr(athlete, "athlete_profile") and athlete.athlete_profile.coach == user

        return False