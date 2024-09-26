from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_youtube_link(value):
    """
    Валидатор проверяет, что ссылка относится к YouTube.
    """
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ["www.youtube.com", "youtube.com", "youtu.be"]:
        raise ValidationError("Можно добавлять ссылки только с YouTube.")
