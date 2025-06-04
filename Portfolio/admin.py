from django.contrib import admin

# Register your models here.

from Portfolio.models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'programming_language', 'created_at')
    list_filter = ('programming_language', 'category', 'created_at')
    search_fields = ('title', 'programming_language', 'category')
    ordering = ('-created_at',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)