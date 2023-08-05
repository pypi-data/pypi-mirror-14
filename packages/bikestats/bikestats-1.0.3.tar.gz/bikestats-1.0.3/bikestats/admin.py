from django.contrib import admin
from bikestats.models import Make, Model, Stat


class MakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'last_modified')
    search_fields = ('id', 'name', 'description', 'last_modified')


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_make', 'years', 'description', 'last_modified')
    search_fields = ('id', 'name', 'get_make', 'years', 'description', 'last_modified')

    def get_make(self, obj):
        return obj.make.name

    get_make.short_description = 'Make'
    get_make.admin_order_field = 'make__name'


class StatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')
    search_fields = ('id', 'name', 'value')


admin.site.register(Make, MakeAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Stat, StatAdmin)
