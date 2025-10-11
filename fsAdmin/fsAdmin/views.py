from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .serializers import UserSerializer


class UserAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        POST /api/user/ → login или logout
        """
        action = request.data.get('action')

        # ----- LOGOUT -----
        if action == "logout":
            response = Response({"detail": "Logged out"})
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response

        # ----- LOGIN -----
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            "detail": "Login successful",
            "user": UserSerializer(user).data
        })

        response.set_cookie(
            key='access',
            value=access_token,
            httponly=True,
            secure=True,  # True ако си на HTTPS
            samesite='None',
            max_age=60 * 30  # 30 мин
        )
        response.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='None',
            max_age=60 * 60 * 24 * 7  # 7 дни
        )
        return response

    def get(self, request, *args, **kwargs):
        """
        GET /api/user/ → профил
        GET /api/user/?action=refresh → обновява токена
        """
        action = request.query_params.get('action')

        if action == "refresh":
            return self._refresh_token(request)

        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(UserSerializer(user).data)

    def _refresh_token(self, request):
        refresh_cookie = request.COOKIES.get('refresh')
        if not refresh_cookie:
            return Response({"detail": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_cookie)
            new_access = str(refresh.access_token)

            response = Response({
                "detail": "Access token refreshed",
                "timestamp": timezone.now()
            })
            response.set_cookie(
                key='access',
                value=new_access,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=60 * 30
            )
            return response
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
