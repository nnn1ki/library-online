from django.db import models

class Section(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание")
    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
    def __str__(self):
        return self.name

class Library(models.Model):
    location = models.CharField(max_length=255, verbose_name="Место")
    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.location

class Catalog(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, verbose_name="Филиал")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Секция")
    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталоги"

    def __str__(self):
        return f"Catalog {self.id} in Library {self.library.location}, Section {self.section.name}"