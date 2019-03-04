from django.contrib import admin
from .models import Landing, LandingImage, TemplateFile, StaticFile


class LandingImageInline(admin.TabularInline):
    model = LandingImage
    extra = 1


@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    inlines = [LandingImageInline]
    prepopulated_fields = {"slug": ("title_page",)}
    list_display = (
        'title', 
        'title_page', 
        'is_landing_active', 
        'date_added', 
        'date_changed'
    )


@admin.register(TemplateFile)
class TemplateFileAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'is_template_active', 'created'
    )


@admin.register(StaticFile)
class StaticFileAdmin(admin.ModelAdmin):
    list_display = (
        'file_name', 'file_type', 'is_file_active', 'created'
    )
