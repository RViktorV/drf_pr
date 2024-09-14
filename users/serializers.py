from rest_framework import serializers
from users.models import Users, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment, который преобразует объекты платежей
    в JSON-формат для вывода в API.

    Поля:
    - id: Идентификатор платежа.
    - user: Пользователь, совершивший платеж.
    - payment_date: Дата совершения платежа.
    - course: Курс, за который был произведен платеж (может быть пустым).
    - lesson: Урок, за который был произведен платеж (может быть пустым).
    - amount: Сумма платежа.
    - payment_method: Способ оплаты (наличные или банковский перевод).
    """

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
    """
    Сериализатор для модели Users, который преобразует объекты пользователей
    в JSON-формат для вывода в API, с добавлением истории платежей.

    Поля:
    - id: Идентификатор пользователя.
    - email: Электронная почта пользователя.
    - phone_number: Номер телефона пользователя.
    - country: Страна проживания пользователя.
    - avatar: Аватар пользователя.
    - city: Город проживания пользователя.
    - payment_history: История платежей пользователя, выводится как список платежей.
    """

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
