# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Location, Game, Tournament, Profile

class GameAdmin(admin.ModelAdmin):
    pass

class LocationAdmin(admin.ModelAdmin):
    exclude = ('lat', 'lng')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'vkontakte_id', 'is_active')
    list_filter = ('is_active',)
    
admin.site.register(Location, LocationAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Tournament)
admin.site.register(Profile, ProfileAdmin)
