from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Categorías de zapatillas (Running, Casual, Basketball, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Modelo de producto para zapatillas"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    sizes = models.CharField(max_length=100, help_text="Tallas disponibles separadas por coma (ej: 38,39,40,41,42)")
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def available_sizes(self):
        """Devuelve lista de tallas disponibles"""
        return [size.strip() for size in self.sizes.split(',') if size.strip()]


class CartItem(models.Model):
    """Item del carrito de compras"""
    session_key = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.product.name} - Talla {self.size} x {self.quantity}"
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.product.price * self.quantity
