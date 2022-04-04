from pyexpat import model
from django.contrib import admin
from .models import Genre
from .models import Filmwork
from .models import GenreFilmwork
from .models import Person
from .models import PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    raw_id_fields = ("person",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created",
        "modified",
    )

    # Поиск по полям
    search_fields = (
        "name",
        "description",
        "id",
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "created",
        "modified",
    )

    # Поиск по полям
    search_fields = ("full_name", "id")


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmWorkInline)

    # Отображение полей в списке
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created",
        "modified",
    )

    # Фильтрация в списке
    list_filter = ("type",)

    # Поиск по полям
    search_fields = ("title", "description", "id")
