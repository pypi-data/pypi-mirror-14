from django.contrib import admin
from bikestats.models import Make, Model, Stat


class MakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'last_modified')
    search_fields = ('id', 'name', 'description', 'last_modified')


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_make', 'year_start', 'year_end', 'description', 'last_modified')
    search_fields = ('id', 'name', 'make__name', 'year_start', 'year_end', 'description', 'last_modified')

    def get_make(self, obj):
        return obj.make.name

    get_make.short_description = 'Make'
    get_make.admin_order_field = 'make__name'


class StatAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_model', 'get_make', 'name', 'value')
    search_fields = ('id', 'model__name', 'model__make__name', 'name', 'value')

    def get_model(self, obj):
        return obj.model.name

    get_model.short_description = 'Model'
    get_model.admin_order_field = 'model__name'

    def get_make(self, obj):
        return obj.model.make.name

    get_make.short_description = 'Make'
    get_make.admin_order_field = 'model__make__name'


admin.site.register(Make, MakeAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Stat, StatAdmin)
