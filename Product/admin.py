from django.contrib import admin
from .models import *




#admin.site.register(Product)
admin.site.register(Category)
admin.site.register(pedido)
admin.site.register(Direccion)
admin.site.register(User)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('Image','name','description','price','category')
    list_display = ("Imagen","name","price","slug","Active")
    list_editable = ("price","Active")
    list_filter = ["category","Active"]
    search_fields = ["name"]
    list_per_page = 3

@admin.register(Inventory)

class InventoryAdmin(admin.ModelAdmin):
    fields = ('Producto',"Intial_stocks","Inputs","Outputs")
    list_display = ("Imagen","Date","Producto","Intial_stocks","Inputs","Outputs","Stock")
    list_filter = ["Producto","Date"]
@admin.register(Califications)

class CalificationAdmin(admin.ModelAdmin):
    fields = ('Producto',"Calification","Comentary")
    list_display = ("Imagen","Date","user","Producto","Calification","Comentary")
    list_filter = ["Producto","Calification","Date"]
    search_fields = ["Producto"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at","direccion","total")



