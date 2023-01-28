from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)


admin.site.register(Category)








