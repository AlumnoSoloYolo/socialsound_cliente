
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
    


