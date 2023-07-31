from django.contrib import admin  # Register your models here.
from main.models import News, Category, Tag, Comment


admin.site.register(News)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

