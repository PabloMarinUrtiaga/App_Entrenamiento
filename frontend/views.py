from django.shortcuts import render, redirect

# Create your views here.

def landing(request):
    # Si ya está logueado, lo mandamos directo a su dashboard según el rol
    if request.user.is_authenticated:
        if request.user.role == "coach":
            return redirect("coach-dashboard")
        return redirect("athlete-dashboard")
    return render(request, "frontend/landing.html")