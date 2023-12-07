"""castilloDeporte URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from Product.urls import *



urlpatterns = [
     path('admin/', admin.site.urls),
     path('', views.index, name='index'),
     path('contacto/', views.contacto,name='contacto'),
     path('Productos/',views.ProductListView.as_view(),name='productos'),
     path('join/',views.login_view,name='join'), 
     path('register/',views.registro,name='registro'),
     path('recordar/',views.recordar,name='recordar'),
     path('logout/', views.logout_view, name='logout'),
     path('tienda/',views.tienda,name= 'tienda'),
     path('cliente/',views.cliente,name='cliente'),
     path('verperfil/',views.verperfil,name='verperfil'),
     path('comentarios/',views.agregarcalificacion,name='comentarios'),
     path('Product/',views.catalogo,name="catalogo"),
     path('agregar/',views.add,name="add"),
     path('eliminar/',views.remove,name="remove"),
     path('order',views.order,name='order'),
     path('direcciones/',views.shippingAdrressListview.as_view(),name="direccion"),
     path('agregard/',views.agregardireccion,name="agregard"),
     path('editar/<int:pk>',views.editardireccionUpdateView.as_view(),name='updated'),
     path('delete/<int:pk>',views.direccionDeleteView.as_view(),name="Delete"),
     path('update/<int:pk>',views.default,name="default"),
     path('direccionpedido/',views.adress,name="direccionpedido"),
     path('direccionpedidoselect/',views.select_address,name="Select"),
     path('establecer/<int:pk>',views.check_direccion,name="establece"),
     path('confirmarpedido/',views.confirm,name="Confirmar"),
     path('Cancelar/',views.cancel,name="cancelar"),
     path('complete/',views.complete,name="complete"),
     path('Pedidos/',views.orderListView.as_view(),name="pedido"),
     path('Deletepedidos/<int:pk>',views.OrderDeleteView.as_view(),name="deletep"),
     path('ordercomplete/',views.orderadminListView.as_view(),name="pedidoadmin"),
     path('miscomentarios/',views.ComentarioListview.as_view(),name="comentario"),
     path('Deletecomentarios/<int:pk>',views.CalificationDeleteView.as_view(),name="deletec"),
     path('Productos/',include('Product.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)