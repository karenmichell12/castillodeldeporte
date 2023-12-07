from django.shortcuts import render 
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect
from Product.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from Product.forms import *
from Product.utils import *
from Product.utils1 import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import *
from django.contrib.auth.decorators import login_required
from django.http import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.shortcuts import *


def index(request): 

    return render(request, 'index.html',{ 


    }) 

def productos(request):
    productos = Product.objects.all()
    data = {
        'productos' : productos
    }
    
    return render(request, 'productos.html', data)
 
def contacto(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        template = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'message': message,
            'subject': subject,
        })
    
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['karenmichell.poveda@gmail.com']
        )
    
        email.fail_silently = False
        email.send()
    
    return render(request, 'Contactenos.html',{

    })
	 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('cliente')
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html',{

    })
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('index')


    
def registro(request):
    data = {
        "form": CustomUserCreationForm()
    }
    formulario = CustomUserCreationForm(data=request.POST)
    if request.method == 'POST':
     if formulario.is_valid():
        formulario.save()
        user = authenticate(username=formulario.cleaned_data["username"],password1=formulario.cleaned_data["password1"])
        messages.success(request,"Te has registrado correctamente")
        return redirect(to="index")
    data["form"] =  formulario
    return render(request,'registro.html',data)

def recordar(request):
    return render(request,'recordarcontraseña.html',{


    })

def agregarcalificacion(request):
    data = {
        'form': CalificationForm()
    }
    if request.method == 'POST':
        formulario = CalificationForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            calificacion = formulario.save(commit=False)
            calificacion.user = request.user
            calificacion.save()
            return redirect('comentario')
    return render(request,'agregarcalificacion.html',data)


class ProductListView(ListView):
    template_name = 'productos.html'
    queryset = Product.objects.all().order_by('-id')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = context ['object_list']
        return context




class ProductDetailView(DetailView):
    model = Product
    template_name = 'productdetail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


def tienda(request):
    cart = get_or_create_cart(request)

    return render (request,'tienda.html',{
        "cart":cart

    })

def add(request):
    pedido = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    #cart.Products.add(product, through_defaults ={
    #    'quantity': quantity
    #})
    cart_product = pedidoproducts.objects.create_or_update_quantity(pedido=pedido,product=product,quantity=quantity)


    return render (request , 'add1.html',{
        'products':product
    })

def remove(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))

    cart.Products.remove(product)

    return redirect('tienda')
    

def cliente(request):
    return render(request,'cliente.html',{


    })


def verperfil(request):
    return render(request,'verperfil.html',{


    })

def catalogo (request):
    productos = Product.objects.all()
    data = {
        'productos' : productos
    }

    return render(request, 'product.html', data)

@login_required(login_url='join')

def order (request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    return render(request,'order.html',{
        'cart':cart,
        'order':order
    }) 

class shippingAdrressListview(ListView,LoginRequiredMixin):
    login_url = 'join'
    model = Direccion
    template_name = 'adress.html'

    def get_queryset(self):
        return Direccion.objects.filter(user=self.request.user).order_by('-default')

@login_required(login_url='join')

def agregardireccion(request):
    data = {
        'form': Direccionform()
    }
    if request.method == 'POST':
        formulario = Direccionform(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            direccion = formulario.save(commit=False)
            direccion.user = request.user
            direccion.default = not request.user.has_direccion()
            direccion.save()
            if request.GET.get('next'):
                if request.GET['next'] == reverse('direccionpedido'):
                    cart = get_or_create_cart(request)
                    order= get_or_create_order(cart,request)

                    order.update_direccion(direccion)

                    return HttpResponseRedirect(request.GET['next'])
                
            return redirect('direccion')
    return render(request,'agregardireccion.html',data)



class editardireccionUpdateView(UpdateView,LoginRequiredMixin):
    login_url = 'join'
    model = Direccion
    form_class = Direccionform
    template_name= 'editardireccion.html'

    def get_success_url(self):
        return reverse('direccion')
    

class direccionDeleteView(DeleteView,LoginRequiredMixin):
    login_url ='login'
    model = Direccion
    template_name='deletedireccion.html'
    success_url=reverse_lazy('direccion')

    def dispatch(self,request,*args,**kwargs):
        if self.get_object().default:
            return redirect('direccion')
        
            
        if request.user.id != self.get_object().user_id:
            return redirect('direccion')
        
        if self.get_object().has_orders():
            return redirect('direccion')
        


@login_required(login_url='join')
def default(request,pk):
    direccion = get_object_or_404(Direccion, pk=pk)

    if request.user.id != direccion.user_id:
        return redirect('direccion')
    
    if request.user.has_direccion():
        request.user.direccion.update_default()
    
    direccion.update_default(True)

    return redirect('direccion')

@login_required(login_url='join')
def adress(request):
    cart= get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    direccion = order.get_or_set_direccion()
    can_choose_direccion = request.user.direccion_set.count() > 1

    return render(request, 'adress1.html', {
        'cart': cart,
        'order': order,
        'direccion': direccion,
        'can_choose_direccion': can_choose_direccion,
    })

@login_required(login_url='join')
def select_address(request):

    direccion = request.user.direccion_set.all()

    return render(request, 'select_addres.html',{
       'direccion': direccion 
    })

@login_required(login_url='join')
def check_direccion(request,pk):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)

    direccion = get_object_or_404(Direccion,pk=pk)


    if request.user.id != direccion.user_id:
        return redirect('direccion')
    
    order.update_direccion(direccion)

    return redirect('direccionpedido')

@login_required(login_url='join')
def confirm(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    direccion = order.direccion

    if direccion is None:
        return redirect('direccion')
    
    return render(request,'confirmorder.html',{
        'cart':cart,
        'order':order,
        'direccion': direccion,
    })

@login_required(login_url='join')
def cancel(request):
    cart= get_or_create_cart(request)
    order = get_or_create_order(cart,request)


    if request.user.id != order.user_id:
        return redirect('tienda')
    
    order.cancel()

    destroy_cart(request)
    destroy_order(request)

    return redirect('catalogo')

@login_required(login_url='join')
def complete(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart,request)
    
    if request.user.id != order.user_id:
        return redirect('tienda')
    
    order.complete()
    destroy_cart(request)
    destroy_order(request)

    return redirect('catalogo')

class orderListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    template_name = 'order1.html'

    def get_queryset(self):
        return self.request.user.orders_completed()


class OrderDeleteView(DeleteView,LoginRequiredMixin):
    login_url ='login'
    model = Order
    template_name='deleteorder.html'
    success_url=reverse_lazy('catalogo')


    


class orderadminListView(LoginRequiredMixin,ListView):
    login_url = 'admin:login'
    template_name = 'order4.html'
    queryset = Order.objects.all().order_by('-id')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = context ['object_list']
        return context

class ComentarioListview(ListView,LoginRequiredMixin):
    login_url = 'join'
    model = Califications
    template_name = 'comentario.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['c'] = context ['object_list']
        return context

class CalificationDeleteView(DeleteView,LoginRequiredMixin):
    login_url ='login'
    model = Califications
    template_name='deletecomentario.html'
    success_url=reverse_lazy('comentario')
    


    









    





