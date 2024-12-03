from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# Сериализатор ввода логина (номера телефона) пользователя
class UserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Номер телефона должен состоять из цифр")
        return value


# Сериализатор ввода кода подтверждения
class AuthCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    auth_code = serializers.CharField(max_length=4)

    def validate_auth_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Вводимый код должен состоять из цифр")
        return value


# Сериализатор получения информации профиля
class ProfileSerializer(serializers.ModelSerializer):
    entered_my_referral = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['phone_number', 'referral_code', 'other_code', 'entered_my_referral']

    def get_entered_my_referral(self, obj):
        users = User.objects.filter(other_code=obj.referral_code)
        return [{'phone_number': user.phone_number} for user in users]


# Сериализатор ввода реферального кода
class ReferralSerializer(serializers.Serializer):
    other_code = serializers.CharField(max_length=6)

    def validate_other_code(self, value):
        if not User.objects.filter(referral_code=value).exists():
            raise serializers.ValidationError("Введенный код не существует.")
        return value