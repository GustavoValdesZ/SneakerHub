from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
import re

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=3, 
        max_length=15,
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Ingrese un nombre válido (solo letras).')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
        label="Nombre"
    )
    last_name = forms.CharField(
        min_length=3, 
        max_length=15,
        validators=[RegexValidator(r'^[a-zA-Z]+$', 'Ingrese un apellido válido (solo letras).')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
        label="Apellido"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        label="Correo Electrónico"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        min_length=4,
        max_length=20,
        help_text="La contraseña debe contener al menos 1 mayúscula, 1 número y 1 carácter especial.",
        label="Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        label="Correo Electrónico"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )
