from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import *
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html , urlencode
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'
    
    def lookups(self, request, model_admin) :
        return [
            ('<10','low')
        ]
        
    def queryset(self, request, queryset: QuerySet) :
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
    
    
    
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['collection']#search option 
    
   
    prepopulated_fields={
        'slug':['title']
    }
    #fields=['title','price','membership','inventory']
    exclude=['promotions']
    list_display=['title','price','membership','inventory_status','collection_title']
    list_per_page=5
    list_editable=['price','membership']
    list_select_related=['collection']
    search_fields=['title']
    list_filter=['title','collection',InventoryFilter]
    
    def collection_title(self,product):
        return product.collection.title
        
    
    def inventory_status(self,product):
        if product.inventory <5:
            return 'Low'
        return 'ok'

    
###### Collection   
@admin.register(Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
    search_fields=['title']
    
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode(
                {'collection__id': str(collection.id)}
            )
            )
        return format_html('<a href="{}">{}</a>', url, collection.products_count )
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )



    
@admin.register(Order)
class OderAdmin(admin.ModelAdmin):
    
    list_display = ['customer','payment_status','placed_at']
    search_fields = ['customer']
    autocomplete_fields = ['customer']
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields=['customer']




admin.site.register(Promotion)


admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
