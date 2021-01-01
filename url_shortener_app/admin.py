from django.contrib import admin

from .models import LongToShort
from .models import UserLocation

# Register your models here.

class LongToShortAdmin(admin.ModelAdmin):
    list_display = ('longurl', 'shorturl', 'visit_count', )

class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('shorturl','city','lat','long',)

admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(LongToShort, LongToShortAdmin)