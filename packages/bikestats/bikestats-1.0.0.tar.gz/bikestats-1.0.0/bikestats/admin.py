from django.contrib import admin
from bikestats.models import Make, Model, Stat


admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Stat)
