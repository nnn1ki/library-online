from django.db import models

class Library(models.Model):
    description = models.TextField(verbose_name="Описание")
    address = models.CharField(max_length=255, verbose_name="Место")

    class Meta:
        verbose_name = "Библиотека"
        verbose_name_plural = "Библиотеки"

    def __str__(self):
        return f"{self.description} {self.address}"

class LibraryDatabase(models.Model):
    database = models.CharField(max_length=255, verbose_name="База данных")
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="databases")

    class Meta:
        verbose_name = "База данных библиотеки"
        verbose_name_plural = "Базы данных библиотек"

    def __str__(self):
        return f"{self.database} - {self.library.name}"