from django.contrib import admin
from django_markdown.models import MarkdownField
from django_markdown.widgets import AdminMarkdownWidget

from shark.models import EditableText, StaticPage


@admin.register(EditableText)
class EditableTextAdmin(admin.ModelAdmin):
    list_display = ['name', 'handler_name', 'last_used']
    list_filter = ['last_used', 'handler_name']
    ordering = ['handler_name', 'name']

    fieldsets = (
        (None, {
            'fields': ('name', 'handler_name')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Enter the content for this text.'
        })
    )


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}

    list_display = ['url_name', 'title']
    ordering = ['url_name']
