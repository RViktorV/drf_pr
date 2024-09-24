from django.core.exceptions import ValidationError
from learning.validators import validate_youtube_link
import pytest

def test_validate_youtube_link():
    # Корректные ссылки
    valid_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ"
    ]
    for link in valid_links:
        try:
            validate_youtube_link(link)
        except ValidationError:
            pytest.fail(f"Validation failed for valid link: {link}")

    # Некорректные ссылки
    invalid_links = [
        "https://vimeo.com/123456789",
        "https://www.example.com/video"
    ]
    for link in invalid_links:
        with pytest.raises(ValidationError):
            validate_youtube_link(link)
