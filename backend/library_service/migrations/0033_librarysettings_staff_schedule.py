from django.db import migrations, models

import library_service.models.library_settings


class Migration(migrations.Migration):
    dependencies = [
        ("library_service", "0032_notification_controls_and_last_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="librarysettings",
            name="staff_digest_schedule_overrides",
            field=models.JSONField(
                default=library_service.models.library_settings.default_staff_digest_schedule_overrides,
                verbose_name="Переопределения рабочих часов для конкретных дат",
            ),
        ),
        migrations.AddField(
            model_name="librarysettings",
            name="staff_digest_week_schedule",
            field=models.JSONField(
                default=library_service.models.library_settings.default_staff_digest_week_schedule,
                verbose_name="Шаблон рабочих часов для рассылки сотрудникам",
            ),
        ),
    ]
