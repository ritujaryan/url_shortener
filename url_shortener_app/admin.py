from django.contrib import admin

from .models import LongToShort
from .models import UserLocation

# Register your models here.

class LongToShortAdmin(admin.ModelAdmin):
    list_display = ('longurl', 'shorturl', 'visit_count', )

class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('shorturl','ip','city','lat','long','date','time',)

admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(LongToShort, LongToShortAdmin)