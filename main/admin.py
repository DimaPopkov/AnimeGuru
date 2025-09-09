from django.contrib import admin
from .models import Product, Category, Tags, Pics, Album_Pics, Status, Weblinks, Voice_maker, Characters

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Pics)
admin.site.register(Album_Pics)
admin.site.register(Status)
admin.site.register(Weblinks)
admin.site.register(Voice_maker)
admin.site.register(Characters)