from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category, CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
import uuid


def home(request):
    """Vista principal - catálogo de productos"""
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    featured_products = Product.objects.filter(featured=True, stock__gt=0)[:4]
    
    # Filtros
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    category_name = None
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
        category = Category.objects.filter(slug=category_slug).first()
        if category:
            category_name = category.name
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(brand__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'featured_products': featured_products,
        'current_category': category_slug,
        'category_name': category_name,
        'search_query': search_query,
    }
    return render(request, 'shop/home.html', context)


def product_detail(request, slug):
    """Vista de detalle de producto"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        stock__gt=0
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


def cart_view(request):
    """Vista del carrito"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.subtotal for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)


def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))
        
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        # Verificar si el item ya existe en el carrito
        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Producto agregado al carrito'
        })
    
    return JsonResponse({'success': False}, status=400)


def update_cart(request, item_id):
    """Actualizar cantidad en el carrito"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({
                'success': True,
                'subtotal': float(cart_item.subtotal)
            })
        
    return JsonResponse({'success': False}, status=400)


def remove_from_cart(request, item_id):
    """Eliminar item del carrito"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create user but commit=False to set username automatically
            user = form.save(commit=False)
            # Use email or uuid as username since we login with email
            user.username = uuid.uuid4().hex[:30] 
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Authenticate and login
            login(request, user)
            return redirect('shop:home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'shop/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Check if user exists with this email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('shop:home')
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
        
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('shop:home')

