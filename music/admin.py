from django.contrib import admin

from .models import Album, Music


class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created_at', )
    list_filter = ('created_at', )


admin.site.register(Album)
admin.site.register(Music, MusicAdmin)