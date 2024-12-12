from django.contrib import admin
from . models import *

class ImageGalleryTabular(admin.TabularInline):
    model = ImageGallery
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ImageGalleryTabular]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
