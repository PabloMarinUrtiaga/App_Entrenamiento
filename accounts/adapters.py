from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoLocalSignupAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Bloquea el registro tradicional (usuario/contraseña)
        return False


class SocialSignupAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Permite que CUALQUIER cuenta de Google nueva se registre
        return True