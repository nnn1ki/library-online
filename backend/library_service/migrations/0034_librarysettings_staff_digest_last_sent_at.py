from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library_service", "0033_librarysettings_staff_schedule"),
    ]

    operations = [
        migrations.AddField(
            model_name="librarysettings",
            name="staff_digest_last_sent_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Когда дайджест сотрудникам был отправлен в последний раз",
            ),
        ),
    ]
