from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('library_service', '0012_alter_basketitem_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibrarySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_books_per_order', models.PositiveIntegerField(default=5, verbose_name='Максимальное количество книг в заказе')),
                ('max_books_per_reader', models.PositiveIntegerField(default=10, verbose_name='Максимальное количество книг на руках')),
                ('max_borrow_days', models.PositiveIntegerField(default=14, verbose_name='Максимальное количество дней на выдачу')),
                ('max_extensions', models.PositiveIntegerField(default=2, verbose_name='Максимальное количество продлений')),
                ('overdue_fine_per_day', models.DecimalField(default=10.00, verbose_name='Штраф за просрочку (в день)', max_digits=6, decimal_places=2)),
                ('holidays', models.JSONField(default=list, verbose_name='Список календарных выходных')),
                ('library', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='library_service.library')),
            ],
            options={
                'verbose_name': 'Настройки библиотеки',
                'verbose_name_plural': 'Настройки библиотек',
            },
        ),
    ]
