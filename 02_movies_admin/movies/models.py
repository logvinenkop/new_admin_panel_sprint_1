import uuid
from operator import mod
from pyexpat import model
from turtle import title
from unicodedata import name
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Класс для описания полей created и modified
class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
    )

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


# Класс для описания поля id
class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


# Класс для описания таблицы genre
class Genre(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.name

    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(
        _("Description"),
        blank=True,
    )

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = 'content"."genre'
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


# Класс для описания представления таблицы person
class Person(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.full_name

    full_name = models.CharField(
        _("Full name"),
        max_length=255,
    )

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


# Класс для описания представления таблицы film_work
class Filmwork(UUIDMixin, TimeStampedMixin):
    def __str__(self):
        return self.title

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(
        _("Description"),
        blank=True,
    )
    creation_date = models.DateField(
        _("Crereation date"),
        blank=True,
    )
    rating = models.FloatField(
        _("Rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _("Type"),
        max_length=10,
        choices=[("movie", "Кино"), ("tv_show", "Сериал")],
        default="movie",
    )

    certificate = models.CharField(
        _("certificate"),
        max_length=512,
        blank=True,
    )

    file_path = models.FileField(
        _("file"),
        blank=True,
        null=True,
        upload_to="movies/",
    )

    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmwork",
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmWork",
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Film work")
        verbose_name_plural = _("Film works")


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        # related_name="id",
        verbose_name=_("Film work"),
    )
    genre = models.ForeignKey(
        "Genre",
        on_delete=models.CASCADE,
        # related_name="id",
        verbose_name=_("Genre"),
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("Filmworks gengre")
        verbose_name_plural = _("Filmworks gengres")


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
        # related_name="id",
        verbose_name=_("Film work"),
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        # related_name="id",
        verbose_name=_("Person"),
    )
    role = models.TextField(_("Role"), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("Filmworks person")
        verbose_name_plural = _("Filmworks persons")
