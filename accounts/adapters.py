from allauth.account.adapter import DefaultAccountAdapter


class NoLocalSignupAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Bloquea el registro tradicional (usuario/contraseña) — solo login con Google
        return False