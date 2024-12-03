import time

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, AuthCodeSerializer, ProfileSerializer, ReferralSerializer
from .models import CustomUser


# Представление для отправки кода подтверждения
class AuthenticationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            user, create = CustomUser.objects.get_or_create(phone_number=phone_number, username=phone_number)

            user.generate_auth_code()
            time.sleep(2)
            print(f'Код авторизации: {user.auth_code}. Для номера: {phone_number}')

            return Response(
                {"message": f"Код ({user.auth_code}) отправлен на указанный номер телефона"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление для проверки кода подтверждения и предоставления информации о профиле пользователя
class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AuthCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            auth_code = serializer.validated_data['auth_code']

            user = CustomUser.objects.get(phone_number=phone_number)
            if user.auth_code == auth_code:
                token, created = Token.objects.get_or_create(user=user)
                profile_serializer = ProfileSerializer(user)
                return Response(
                    {
                        "message": "Код подтвержден",
                        "token": token.key,
                        "profile": profile_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Неверный код"},
                    status=status.HTTP_403_FORBIDDEN
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление профиля пользователя
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


# Представление для проверки ввода реферального кода и предоставления информации о профиле пользователя
class ReferralInputView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReferralSerializer(data=request.data)
        if serializer.is_valid():
            other_code = serializer.validated_data['other_code']
            user = request.user

            if user.other_code is None:
                user.other_code = other_code
                user.save()
                profile_serializer = ProfileSerializer(user)
                return Response(
                    {
                        "message": "Код успешно введен.",
                        "profile": profile_serializer.data
                    }, status=status.HTTP_200_OK)
            return Response({"error": "Реферальный код уже введен."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)