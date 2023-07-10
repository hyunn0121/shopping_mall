from django.contrib import admin
from .models import Item, Category, Manufacturer, Tag, Comment

# Register your models here.
admin.site.register(Item)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)

admin.site.register(Manufacturer)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)

