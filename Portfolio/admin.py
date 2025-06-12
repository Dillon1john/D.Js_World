from django.contrib import admin

# Register your models here.

from Portfolio.models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'category')
    ordering = ('-created_at',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Language, LanguageAdmin)