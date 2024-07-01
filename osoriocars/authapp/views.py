from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm, ContactForm, ServiceForm
from .models import Service, Cart, CustomUser,Order
from django.shortcuts import render
from .models import CustomUser, Order
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ServiceForm
from .models import Service


User = get_user_model()

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        order.services.set(cart.services.all())
        order.calculate_total()  # Calcula el total después de establecer los servicios
        cart.services.clear()  # Clear the cart after checkout
        return redirect('order_detail', order_id=order.id)
    return render(request, 'checkout.html', {'cart': cart})

def index_view(request):
    services = Service.objects.all()
    return render(request, 'index.html', {'services': services})

def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.services.add(service)
    return redirect('servicios')


@login_required(login_url='/login/')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    services = cart.services.all()
    total = sum(service.price for service in services)
    return render(request, 'cart.html', {'cart': cart, 'services': services, 'total': total})


def remove_from_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.services.remove(service)
    return redirect('view_cart')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def admin_required(login_url='/login/'):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)

def services_view(request):
    services = Service.objects.all()
    return render(request, 'servicios.html', {'services': services})

@login_required
@user_passes_test(lambda u: u.is_mechanic)
def manage_services(request):
    services = Service.objects.all()
    return render(request, 'manage_services.html', {'services': services})

@login_required
@user_passes_test(lambda u: u.is_mechanic)
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio agregado correctamente.')
            return redirect('manage_services')
    else:
        form = ServiceForm()
    return render(request, 'add_service.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_mechanic)
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('manage_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_service.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_mechanic)
def remove_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('manage_services')
    return render(request, 'remove_service.html', {'service': service})

@login_required
@admin_required(login_url='/login/')
def admin_dashboard(request):
    users = CustomUser.objects.all()
    orders_by_user = {user.id: Order.objects.filter(user=user) for user in users}

    return render(request, 'admin-dashboard.html', {
        'users': users,
        'orders_by_user': orders_by_user,
    })

@login_required
@admin_required(login_url='/login/')
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_dashboard')



@login_required
@admin_required(login_url='/login/')
def toggle_mechanic_status(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    user.is_mechanic = not user.is_mechanic
    user.save()
    return redirect('admin_dashboard')

@login_required
@admin_required(login_url='/login/')
def delete_user(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    user.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('admin_dashboard')

@login_required
@admin_required(login_url='/login/')
def edit_user(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario modificado exitosamente.')
            return redirect('admin_dashboard')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    return render(request, 'contacto.html', {'form': form})

def about_view(request):
    return render(request, 'sobre.html', {'user': request.user})

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'orders': orders})
    