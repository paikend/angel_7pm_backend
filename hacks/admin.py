from django.contrib import admin
from .models import *


class HacksAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'title', 'created_at' ]
admin.site.register(Hacks, HacksAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'name', 'created_at' ]
admin.site.register(Team, TeamAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'user', 'hacks', 'team','created_at' ]
admin.site.register(Application, ApplicationAdmin)