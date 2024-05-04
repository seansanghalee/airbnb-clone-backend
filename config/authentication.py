from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

# runs before views, this is what returns User


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        trusted = request.headers["Trust-Me"] == "bro!"
        if trusted:
            username = request.headers["username"]
            if not username:
                return None
            try:
                user = User.objects.get(username=username)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed
