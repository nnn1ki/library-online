from django.db import migrations, models

import library_service.models.library_settings


class Migration(migrations.Migration):
    dependencies = [
        ("library_service", "0031_userprofile_current_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="librarysettings",
            name="reader_notification_statuses",
            field=models.JSONField(
                default=library_service.models.library_settings.default_reader_notification_statuses,
                verbose_name="Статусы заказа для уведомления читателя",
            ),
        ),
        migrations.AddField(
            model_name="librarysettings",
            name="reader_status_notifications_enabled",
            field=models.BooleanField(
                default=True,
                verbose_name="Отправлять читателю уведомления об изменении статуса заказа",
            ),
        ),
        migrations.AddField(
            model_name="librarysettings",
            name="staff_digest_enabled",
            field=models.BooleanField(
                default=True,
                verbose_name="Отправлять сотрудникам уведомления о необработанных заказах",
            ),
        ),
        migrations.AddField(
            model_name="librarysettings",
            name="staff_notification_active_hours",
            field=models.FloatField(
                default=2,
                verbose_name="Сотрудник считается недавно активным (в часах)",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="staff_notification_mode",
            field=models.CharField(
                choices=[
                    ("auto", "По активности"),
                    ("always", "Всегда получать"),
                    ("disabled", "Не получать"),
                ],
                default="auto",
                max_length=16,
                verbose_name="Режим получения уведомлений о необработанных заказах",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="last_seen",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Последняя активность",
            ),
        ),
    ]
