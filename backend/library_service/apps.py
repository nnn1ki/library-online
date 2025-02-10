from django.apps import AppConfig


class LibraryServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library_service"

    def ready(self):
        import library_service.signals  # pylint: disable=import-outside-toplevel
