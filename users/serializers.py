from rest_framework import serializers
from users.models import Users, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "payment_method",
        ]


class UsersSerializer(serializers.ModelSerializer):
    # История платежей пользователя
    payment_history = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = Users
        fields = [
            "id",
            "email",
            "phone_number",
            "country",
            "avatar",
            "city",
            "payment_history",
        ]
