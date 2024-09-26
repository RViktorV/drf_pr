from django_filters import rest_framework as filters
from users.models import Payment


class PaymentFilter(filters.FilterSet):
    """
    Фильтр для модели Payment, используемый в API для фильтрации платежей.

    Позволяет:
    - Фильтровать платежи по курсу с использованием точного совпадения ID курса.
    - Фильтровать платежи по уроку с использованием точного совпадения ID урока.
    - Фильтровать платежи по способу оплаты с выбором из доступных методов оплаты.
    """

    # Фильтр по точному совпадению ID курса
    course = filters.NumberFilter(field_name="course__id", lookup_expr="exact")

    # Фильтр по точному совпадению ID урока
    lesson = filters.NumberFilter(field_name="lesson__id", lookup_expr="exact")

    # Фильтр по способу оплаты, выбирается из вариантов, определенных в модели Payment
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        """
        Метакласс для указания связанной модели и полей, по которым можно фильтровать.

        - model: Payment — модель, для которой настраивается фильтрация.
        - fields: перечисление полей, по которым возможна фильтрация.
        """

        model = Payment
        fields = ["course", "lesson", "payment_method"]
