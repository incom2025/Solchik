from django.contrib import admin
from .models import Filing, Vyrib, Product, ProductInstance, OrderRequest, Review

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'views', 'order_clicks', 'sentiment_score', 'created_at')
    list_filter = ('filings', 'vyrib', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductInstanceInline]

@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'phone', 'amount', 'source', 'utm_source', 'created_at')
    list_filter = ('source', 'utm_source', 'created_at')
    search_fields = ('name', 'phone', 'message')

admin.site.register(Filing)
admin.site.register(Vyrib)
admin.site.register(ProductInstance)
admin.site.register(Review)
