# Generated by Django 4.2 on 2024-09-18 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0004_merge_20240918_0820"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="preview",
            field=models.ImageField(
                blank=True, null=True, upload_to="course_previews/"
            ),
        ),
    ]
