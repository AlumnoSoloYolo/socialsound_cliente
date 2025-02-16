
from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils import timezone
from .helpers import helper
import re



class BusquedaUsuarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)


class BusquedaAvanzadaUsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(
        label='Nombre usuario',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar usuario por nombre...'
        })
    )
    ciudad = forms.CharField(
        label='Ciudad',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por ciudad...'
        })
    )
    edad_min = forms.IntegerField(
        label='Edad mínima',
        required=False,
        min_value=1,  
        max_value=120,  
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Edad mínima...'
        })
    )
    edad_max = forms.IntegerField(
        label='Edad máxima',
        required=False,
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Edad máxima...'
        })
    )
    bio_contains = forms.CharField(
        label='Buscar según biografía',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en la biografía'
        })
    )
    

class BusquedaAvanzadaAlbumForm(forms.Form):
    titulo = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título'
        })
    )
    artista = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por artista'
        })
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class BusquedaAvanzadaCancionForm(forms.Form):
    titulo = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título'
        })
    )
    
    artista = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por artista'
        })
    )
    
    CATEGORIAS_CHOICES = [
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        ('metal', 'Metal'),
        ('electronica', 'Electrónica'),
        ('pop', 'Pop'),
        ('hiphop', 'Hip-Hop'),
        ('reggae', 'Reggae'),
        ('blues', 'Blues'),
        ('classical', 'Clásica'),
        ('country', 'Country'),
        ('dance', 'Dance'),
        ('disco', 'Disco'),
        ('dubstep', 'Dubstep'),
        ('edm', 'EDM'),
        ('funk', 'Funk'),
        ('gospel', 'Gospel'),
        ('indie', 'Indie'),
        ('latin', 'Latina'),
        ('punk', 'Punk'),
        ('rap', 'Rap'),
        ('reggaeton', 'Reggaetón'),
        ('rock', 'Rock'),
        ('soul', 'Soul'),
        ('trap', 'Trap')
    ]

    etiqueta = forms.ChoiceField(
        choices=[('', 'Todas las categorías')] + CATEGORIAS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    album = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por álbum'
        })
    )


class BusquedaAvanzadaPlaylistForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre de playlist'
        })
    )
    
    usuario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre de usuario'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    publica = forms.ChoiceField(
        choices=[('', 'Todas'), ('True', 'Públicas'), ('False', 'Privadas')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )



class UsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(
        label="Nombre de Usuario",
        required=True, 
        max_length=100,
        help_text="100 caracteres como máximo"
    )
    
    email = forms.EmailField(
        label="Email",
        required=True, 
        help_text="Introduce un email válido"
    )
    
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(),
        help_text="Mínimo 8 caracteres, debe incluir mayúscula, minúscula, número y carácter especial"
    )
    
    bio = forms.CharField(
        label="Biografía",
        required=False,
        widget=forms.Textarea()
    )
    
    foto_perfil = forms.FileField(
        label="Foto de Perfil",
        required=False
    )

    def clean_nombre_usuario(self):
        nombre = self.cleaned_data['nombre_usuario']
        if len(nombre) < 4:
            raise forms.ValidationError("El nombre debe tener al menos 4 caracteres")
        if not nombre.isalnum():
            raise forms.ValidationError("El nombre solo puede contener letras y números")
        if any(char.isupper() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener mayúsculas")
        return nombre

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        if not re.search("[a-z]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos una minúscula")
        if not re.search("[A-Z]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos una mayúscula")
        if not re.search("[0-9]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos un número")
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("La contraseña debe incluir al menos un carácter especial")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Introduce un email válido")
        if not any(x.isupper() for x in email.split('@')[0]):
            raise forms.ValidationError("El email debe contener al menos una mayúscula antes del @")
        if len(email.split('@')[0]) < 4:
            raise forms.ValidationError("El email debe tener al menos 4 caracteres antes del @")
        return email
    
   


