from django.contrib import admin

from .models import LongToShort

# Register your models here.

class LongToShortAdmin(admin.ModelAdmin):
    list_display = ('longurl', 'shorturl', 'visit_count', )

admin.site.register(LongToShort, LongToShortAdmin)