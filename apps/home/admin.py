from django.contrib import admin
from django.utils.html import format_html

from apps.home.models import Werkjaar


@admin.register(Werkjaar)
class WerkjaarAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['__str__', 'yearTheme', 'year_theme_logo_image', 'year_theme_song_url']

    @staticmethod
    def year_theme_song_url(werkjaar):
        if werkjaar.yearThemeSong:
            return format_html(f'<a href="{werkjaar.yearThemeSong}" '
                               f'target="blank">{werkjaar.yearThemeSong}</a>')

    @staticmethod
    def year_theme_logo_image(werkjaar):
        if werkjaar.yearThemeLogo:
            return format_html(f'<a href="{werkjaar.yearThemeLogo.url}" target="blank">'
                               f'<img src="{werkjaar.yearThemeLogo.url}" '
                               f'alt="{werkjaar.yearTheme}" '
                               f'width="100" height="200"></a>')
