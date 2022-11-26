from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.
# admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Client)
admin.site.register(Order)


def update_stock(modeladmin, request, queryset):
    for obj in queryset:
        obj.stock += 50
        obj.save()


update_stock.short_description = 'Add 50 to stock'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [update_stock]


class ClientAdmin(admin.ModelAdmin):
    def list_of_categories(obj):
        return list(obj.interested_in.all())

    list_display = ('first_name', 'last_name', 'city', list_of_categories)


admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
