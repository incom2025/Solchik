from django.contrib import admin

# Зареєструйте свої моделі тут.
from .models import Vyrib, Filing, Product, ProductInstance

#admin.site.register(Product)
#admin.site.register(Vyrib)
admin.site.register(Filing)
#admin.site.register(ProductInstance)

# Визначте клас адміністратора
class VyribAdmin(admin.ModelAdmin):
    list_display = ('decor_name', 'first_name', 'date_of_creation') 
    fields = ['first_name', 'decor_name', ('date_of_creation')]
# Зареєструйте клас адміністратора з пов’язаною моделлю
admin.site.register(Vyrib, VyribAdmin)

# Зареєструйте класи адміністратора для Product за допомогою декоратора

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'vyrib', 'applied_filing')
    inlines = [ProductInstanceInline]


# Зареєструйте класи адміністратора для ProductInstance за допомогою декоратора

@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'booked', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('product','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )





