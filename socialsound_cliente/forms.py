
from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils import timezone



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


