
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
    

class UsuarioUpdateForm(forms.Form):
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Introduce un email válido")
        if not any(x.isupper() for x in email.split('@')[0]):
            raise forms.ValidationError("El email debe contener al menos una mayúscula antes del @")
        if len(email.split('@')[0]) < 4:
            raise forms.ValidationError("El email debe tener al menos 4 caracteres antes del @")
        return email
    

class UsuarioActualizarNombreForm(forms.Form):
    nombre_usuario = forms.CharField(
        label="Nombre de Usuario",
        required=True, 
        max_length=100,
        help_text="100 caracteres como máximo"
    )


from .helpers import helper


class AlbumForm(forms.Form):
    titulo = forms.CharField(max_length=200, required=True)
    artista = forms.CharField(max_length=200, required=True)
    portada = forms.ImageField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        usuarios_disponibles = helper.obtener_usuarios_select()
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuarios_disponibles,
            widget=forms.Select,
            required=True,
        )

    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get('titulo')
        artista = cleaned_data.get('artista')
        descripcion = cleaned_data.get('descripcion')
        usuario = cleaned_data.get('usuario')

        if titulo:
            if len(titulo) < 3:
                self.add_error('titulo', 'El título debe tener al menos 3 caracteres')
            if len(titulo) > 200:
                self.add_error('titulo', 'El título no puede exceder los 200 caracteres')

        if artista:
            if len(artista) < 2:
                self.add_error('artista', 'El nombre del artista debe tener al menos 2 caracteres')
            if len(artista) > 200:
                self.add_error('artista', 'El nombre del artista no puede exceder los 200 caracteres')

        if descripcion and len(descripcion) > 1000:
            self.add_error('descripcion', 'La descripción no puede exceder los 1000 caracteres')

        if not usuario:
            self.add_error('usuario', 'Debe seleccionar un usuario')

        return cleaned_data
    

class AlbumUpdateForm(forms.Form):
    titulo = forms.CharField(max_length=200, required=True)
    artista = forms.CharField(max_length=200, required=True)
    portada = forms.ImageField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    
    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get('titulo')
        artista = cleaned_data.get('artista')

        if titulo and len(titulo) < 3:
            self.add_error('titulo', 'El título debe tener al menos 3 caracteres')
            
        if artista and len(artista) < 2:
            self.add_error('artista', 'El artista debe tener al menos 2 caracteres')

        return cleaned_data
    

class AlbumActualizarTituloForm(forms.Form):
    titulo = forms.CharField(
        label="Título",
        max_length=200,
        required=True,
        help_text="Nuevo título del álbum"
    )


class PlaylistForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        required=True,
        help_text="Nombre de la playlist"
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea,
        required=True,
        help_text="Descripción de la playlist"
    )
    publica = forms.BooleanField(
        label="Pública",
        required=False,
        initial=True
    )
    
    def __init__(self, *args, **kwargs):
        super(PlaylistForm, self).__init__(*args, **kwargs)
        
        usuarios_disponibles = helper.obtener_usuarios_select()
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuarios_disponibles,
            widget=forms.Select,
            required=True,
            label="Usuario"
        )
        
        canciones_disponibles = helper.obtener_canciones_select()
        self.fields['canciones'] = forms.MultipleChoiceField(
            choices=canciones_disponibles,
            widget=forms.SelectMultiple,
            required=True,
            label="Canciones",
            help_text="Mantén pulsada la tecla control para seleccionar varias canciones"
        )

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        descripcion = cleaned_data.get('descripcion')
        canciones = cleaned_data.get('canciones')

        if nombre and len(nombre) < 3:
            self.add_error('nombre', 'El nombre debe tener al menos 3 caracteres')

        if descripcion and len(descripcion) < 10:
            self.add_error('descripcion', 'La descripción debe tener al menos 10 caracteres')

        if canciones and len(canciones) < 1:
            self.add_error('canciones', 'Debe seleccionar al menos una canción')

        return cleaned_data
    

class PlaylistUpdateForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        required=True
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea,
        required=True
    )
    publica = forms.BooleanField(
        label="Pública",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(PlaylistUpdateForm, self).__init__(*args, **kwargs)

      
        canciones_disponibles = helper.obtener_canciones_select()
        self.fields['canciones'] = forms.MultipleChoiceField(
            choices=canciones_disponibles,
            widget=forms.SelectMultiple,
            required=True,
            label="Canciones"
        )

        if self.initial.get('canciones'):
            self.fields['canciones'].initial = self.initial['canciones']


class PlaylistActualizarCancionesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlaylistActualizarCancionesForm, self).__init__(*args, **kwargs)
        
        canciones_disponibles = helper.obtener_canciones_select()
        self.fields['canciones'] = forms.MultipleChoiceField(
            choices=canciones_disponibles,
            widget=forms.SelectMultiple,
            required=True,
            label="Canciones",
            help_text="Mantén pulsada la tecla control para seleccionar varias canciones"
        )

        if self.initial.get('canciones'):
            self.fields['canciones'].initial = self.initial['canciones']

    def clean_canciones(self):
        canciones = self.cleaned_data.get('canciones')
        if not canciones or len(canciones) < 1:
            raise forms.ValidationError("Debe seleccionar al menos una canción")
        return canciones


class LikeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LikeForm, self).__init__(*args, **kwargs)
        
        usuarios_disponibles = helper.obtener_usuarios_select()
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuarios_disponibles,
            widget=forms.Select,
            required=True,
            label="Usuario"
        )
        
        canciones_disponibles = helper.obtener_canciones_select()
        self.fields['cancion'] = forms.ChoiceField(
            choices=canciones_disponibles,
            widget=forms.Select,
            required=True,
            label="Canción"
        )


class LikeDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LikeDeleteForm, self).__init__(*args, **kwargs)
        
        usuarios_disponibles = helper.obtener_usuarios_select()
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuarios_disponibles,
            widget=forms.Select,
            required=True,
            label="Usuario"
        )
        
        canciones_disponibles = helper.obtener_canciones_select()
        self.fields['cancion'] = forms.ChoiceField(
            choices=canciones_disponibles,
            widget=forms.Select,
            required=True,
            label="Canción"
        )













class CancionPlaylistForm(forms.Form):
    playlist = forms.ChoiceField(
        label="Playlist",
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super(CancionPlaylistForm, self).__init__(*args, **kwargs)
        
        playlists_disponibles = helper.obtener_playlists_select()
        self.fields['playlist'] = forms.ChoiceField(
            choices=playlists_disponibles,
            widget=forms.Select,
            required=True,
            label="Playlist"
        )
        
        canciones_disponibles = helper.obtener_canciones_select()
        self.fields['canciones'] = forms.MultipleChoiceField(
            choices=canciones_disponibles,
            widget=forms.SelectMultiple,
            required=True,
            label="Canciones",
            help_text="Selecciona las canciones para la playlist"
        )

        # Si hay una playlist seleccionada, marcamos sus canciones
        if self.data.get('playlist'):
            canciones_actuales = helper.obtener_canciones_playlist(self.data['playlist'])
            self.initial['canciones'] = canciones_actuales



class DetalleAlbumForm(forms.Form):
    productor = forms.CharField(max_length=200)
    estudio_grabacion = forms.CharField(max_length=200, required=False)
    numero_pistas = forms.IntegerField()
    sello_discografico = forms.CharField(max_length=100, required=False)
    
    def __init__(self, *args, **kwargs):
        super(DetalleAlbumForm, self).__init__(*args, **kwargs)
        
        albumes_disponibles = helper.obtener_albumes_select()
        self.fields["album"] = forms.ChoiceField(
            choices=albumes_disponibles,
            widget=forms.Select,
            required=True,
        )


class DetalleAlbumUpdateForm(forms.Form):
    productor = forms.CharField(max_length=200)
    estudio_grabacion = forms.CharField(max_length=200, required=False)
    numero_pistas = forms.IntegerField()
    sello_discografico = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(DetalleAlbumUpdateForm, self).__init__(*args, **kwargs)
        
        albumes_disponibles = helper.obtener_albumes_select()  # Recupera las opciones de álbumes

        # Si 'album' está en 'initial', entonces se pasa el valor inicial para el campo de 'album'
        self.fields["album"] = forms.ChoiceField(
            choices=albumes_disponibles,
            widget=forms.Select,
            required=True,
        )

   


