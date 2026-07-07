from django.contrib import admin
from .models import Pattern


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at")