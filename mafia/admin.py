# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Location, Game, Tournament

class GameAdmin(admin.ModelAdmin):
  pass

admin.site.register(Location)
admin.site.register(Game)
admin.site.register(Tournament)
