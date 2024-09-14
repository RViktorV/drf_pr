from django_filters import rest_framework as filters
from users.models import Payment


class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name="course__id", lookup_expr="exact")
    lesson = filters.NumberFilter(field_name="lesson__id", lookup_expr="exact")
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method"]
