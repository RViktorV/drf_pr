from django.contrib import admin
from .models import Course, Lesson


# Регистрация модели Course в админке
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "preview",
        "owner",
    )  # Поля, которые будут отображаться в списке
    search_fields = ("title", "description")  # Поля, по которым можно будет искать


# Регистрация модели Lesson в админке
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "description",
        "preview",
        "owner",
    )  # Поля, которые будут отображаться в списке
    search_fields = ("title", "course__title")  # Поля, по которым можно будет искать
    list_filter = ("course",)  # Фильтры по полю курса
