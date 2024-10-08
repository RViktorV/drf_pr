from rest_framework import serializers
from users.models import Users, Payment


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]  # Добавляем пароль

    # Открытое поле пароля только при создании или обновлении пользователя
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Users(**validated_data)
        user.set_password(password)  # Шифруем пароль
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("payment_method", "session_id", "link", "user")
