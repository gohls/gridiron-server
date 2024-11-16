from knox.auth import TokenAuthentication

class KnoxCookieAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('knox_token')
        if token:
            user = self.authenticate_credentials(token.encode("utf-8"))
            return (user, token)
        return None