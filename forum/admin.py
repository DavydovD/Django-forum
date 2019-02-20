from django.contrib import admin
from .models import(
    Profile,
    SubCategory,
    Category,
    Topic,
    Comment,
)
# Register your models here.


admin.site.register(Profile)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Comment)
