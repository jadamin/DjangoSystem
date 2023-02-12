from django.contrib import admin
from .models import * 
from BetterYou.models import Book

# Register your models here.
from django.contrib.admin import ModelAdmin

class BookAdmin(ModelAdmin):
    # your customizations here
    list_display = ('title', 'author','publication_date')
    search_fields = ('title', 'author')
    ordering = ('publication_date',)

admin.site.register(Book, BookAdmin)
admin.site.register(Appointement)
