from enum import Enum
from random import choices
from unicodedata import decimal
from decimal import *
from urllib import request
import uuid
from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
import decimal
from django.utils.text import slugify


class User(AbstractUser):
    @property

    def direccion(self):
        return self.direccion_set.filter(default=True).first()

    def has_direccion(self):
        return self.direccion is not None
    
    def orders_completed(self):
        return self.order_set.filter(status = orderstatus.COMPLETED).order_by('-id')

    def calificacion(self):
        return self.calificacion_set.filter(user = request.user).oder_by('-id')
    
 
    


class Customer(User):
    class Meta:
        proxy = True
    
    def get_products(self):
        return[]
    
class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(max_length=500,verbose_name="Descripción",null=True,blank=True)
    
 
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "Categoria"
        ordering = ["id"]
 
class Product(models.Model):
    Image = models.ImageField('Imagen del producto',upload_to="media")
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(max_length=500,verbose_name="Descripción",null=True,blank="True")
    price = models.IntegerField(verbose_name="Precio")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(null=False,blank=False)
    Active = models.BooleanField(verbose_name='Activo',default=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args,**kwargs)
    
    def Imagen(self):
      return format_html ( '<img src= {} width="130" height="100" />', self.Image.url )

    
    def __str__(self):
        return self.name
    
   
 
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "producto"
        ordering = ["id"]

class Inventory(models.Model):
    Date = models.DateField('Dia del invetario',auto_now_add=True,null=True,blank=True)
    Producto = models.ForeignKey(Product,on_delete=models.CASCADE)
    Intial_stocks = models.PositiveIntegerField('Existencias iniciales' )
    Inputs = models.PositiveIntegerField('Entradas')
    Outputs = models.PositiveIntegerField('Salidas')
    Stock = models.PositiveIntegerField('Stock',null=True,blank=True)

    def Imagen(self):
     return format_html('<img src= {} width="130" height="100" />',self.Producto.Image.url )
     
    @property
    def calculate_stock(self):
        Stock = self.Intial_stocks + self.Inputs - self.Outputs
        return Stock
    
    def save(self,*args,**kwargs):
        self.Stock = self.calculate_stock
        super(Inventory,self).save(*args,**kwargs)
    

 
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ["id"]

Opciones_de_calificacion = [
    ['Excelente',"Excelente"],
    ['Bueno',"Bueno"],
    ['Regular',"Regular"],
    ['Malo',"Malo"],
    ['Muy malo',"Muy malo"],
]



class Califications(models.Model):
    Date = models.DateTimeField('Dia y hora de la calificacion',auto_now_add=True,null=True,blank=True)
    user = models.ForeignKey(User,null =True,blank=True,on_delete=models.CASCADE)
    Producto = models.ForeignKey(Product,on_delete=models.CASCADE)
    Calification = models.CharField(choices=Opciones_de_calificacion,max_length=100)
    Comentary = models.TextField("Comentario",blank= True,null=True)
    def Imagen(self):
     return format_html('<img src= {} width="130" height="100" />',self.Producto.Image.url )
    

    class Meta:
        verbose_name = "Calificacion"
        verbose_name_plural = "Calificaciones"
        db_table = "Calificacion"
        ordering = ["id"]


ciudad = [
    [0,'Bogota'],
    [1,'Medellin'],
    [2,'Cucuta'],
    [3,'Tunja'],
    [4,'Pereira'],
    [5,'Bucuramanga'],
]
class pedido(models.Model):
    tienda_id = models.CharField(max_length=100,null=False,blank=False,unique=True)
    user = models.ForeignKey(User,null = True,blank=True,on_delete=models.CASCADE)
    Products = models.ManyToManyField(Product,through='pedidoproducts')
    subtotal = models.DecimalField(default=0.0,max_digits=8,decimal_places=2)
    total = models.DecimalField(default=0.0,max_digits=8,decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    FEE= 0.05

    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        order = self.order_set.first()
        if order:
            order.update_total()
    
    def update_subtotal(self):
        self.subtotal = sum([ 
           cp.quantity * cp.product.price for cp in self.products_related()
        ])
        self.save()

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(pedido.FEE))
        self.save()

    def products_related(self):
        return self.pedidoproducts_set.select_related('product')



    def __str__(self):
        return self.tienda_id
    
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = "pedido"
        ordering = ["id"]


class pedidoproductsmanager(models.Manager):
    def create_or_update_quantity(self,pedido,product,quantity = 1):
     object , created =self.get_or_create(pedido=pedido,product=product)

     if not created:
        quantity = object.quantity + quantity

     object.update_quantity(quantity)
    
     return object

class pedidoproducts(models.Model):
    pedido = models.ForeignKey(pedido,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = pedidoproductsmanager()

    def update_quantity(self,quantity=1):
        self.quantity = quantity
        self.save()
    

def set_tienda_id(sender, instance, *args,**kwargs):
     if not instance.tienda_id:
        instance.tienda_id = str(uuid.uuid4())

def update_totals(sender,instance,action,*args,**kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def post_save_update_totals(sender,instance,*args,**kwargs):
    instance.pedido.update_totals()
pre_save.connect(set_tienda_id,sender=pedido)
post_save.connect(post_save_update_totals, sender=pedidoproducts)
m2m_changed.connect(update_totals,sender=pedido.Products.through)


class orderstatus(Enum):
    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in orderstatus]

class Direccion(models.Model):
    user = models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200,verbose_name="Direccion")
    line2= models.CharField(max_length=200,blank=True, verbose_name="Casa/apartamento")
    city = models.CharField(max_length=100,verbose_name="Ciudad")
    state = models.CharField(max_length=100,verbose_name="Barrio")
    postal_code = models.CharField(max_length=30,null=False,blank=False,verbose_name="Telefono")


    default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_orders(self):
        return self.order_set.count() >=1
    def update_default(self,default=False):
        self.default = default
        self.save()

    def __str__(self):
        return self.postal_code

class Order(models.Model):
    order_id = models.CharField(max_length=100,null=False,blank=False,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ForeignKey(pedido,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=choices,default=orderstatus.CREATED)



    shipping_total = models.DecimalField(default=5000,max_digits=8,decimal_places=2)
    total = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  
    direccion = models.ForeignKey(Direccion, null=True, blank=True, on_delete=models.CASCADE)

    def set_total(self):
        return self.cart.total + self.shipping_total
    
    def update_direccion(self,direccion):
        self.direccion = direccion
        self.save()

    def get_or_set_direccion(self):
        if self.direccion:
            return self.direccion
        
        direccion = self.user.direccion
        if direccion:
            self.update_direccion(direccion)

        return direccion
    
    def cancel(self):
        self.status = orderstatus.CANCELED
        self.save()
    
    def complete(self):
        self.status = orderstatus.COMPLETED
        self.save()

    def update_total(self):
        self.total = self.set_total()
        self.save()
    def __str__(self):
        return self.order_id
    
def set_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender,instance,*args,**kwargs):
    instance.total = instance.set_total()


pre_save.connect(set_order_id,sender=Order)
pre_save.connect(set_total,sender=Order)

