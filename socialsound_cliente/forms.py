
from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils import timezone



class BusquedaUsuarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)


# class BusquedaAvanzadaUsuarioForm(forms.Form):
#     nombre_usuario = forms.CharField(
#         label='Nombre usuario',
#         max_length=100,
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Buscar usuario por nombre...'
#         })
#     )
#     ciudad = forms.CharField(
#         label='Ciudad',
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Buscar por ciudad...'
#         })
#     )
#     edad_min = forms.IntegerField(
#         label='Edad mínima',
#         required=False,
#         min_value=1,  
#         max_value=120,  
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Edad mínima...'
#         })
#     )
#     edad_max = forms.IntegerField(
#         label='Edad máxima',
#         required=False,
#         min_value=1,
#         max_value=120,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Edad máxima...'
#         })
#     )
#     bio_contains = forms.CharField(
#         label='Buscar según biografía',
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Buscar en la biografía'
#         })
#     )

#     def clean(self):
#         cleaned_data = super().clean()


#         if not any(cleaned_data.values()):
#             raise forms.ValidationError("Debes especificar al menos un criterio de búsqueda")

#         edad_min = cleaned_data.get('edad_min')
#         edad_max = cleaned_data.get('edad_max')

     
#         if edad_min and not edad_max:
#             cleaned_data['edad_max'] = edad_min
#         elif edad_max and not edad_min:
#             cleaned_data['edad_min'] = edad_max

 
#         if edad_min and edad_max and edad_min > edad_max:
#             raise forms.ValidationError("La edad mínima no puede ser mayor que la edad máxima")


#         if edad_min:
#             cleaned_data['fecha_max'] = date.today().replace(year=date.today().year - edad_min)
#         if edad_max:
#             cleaned_data['fecha_min'] = date.today().replace(year=date.today().year - edad_max - 1)

#         return cleaned_data
    


