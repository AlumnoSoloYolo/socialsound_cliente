from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .forms import *
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
import base64

import json
from django.contrib import messages


def formato_respuesta(response):
    if response.headers['Content-Type'] == 'application/json':
        return response.json()
    
    elif response.headers['Content-Type'] == 'application/xml':
        return ET.fromstring(response.content)
    
    else:
        raise ValueError('Unsupported content type: {}'.format(response.headers['Content-Type']))



def index(request):
    return render(request, "index.html");

def lista_playlists_api(request): 
  
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    response = requests.get(f"{settings.API_URL}playlists", headers=headers)
    playlists = formato_respuesta(response)
    # print(f'{playlists}')
    for playlist in playlists:

        playlist['usuario']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{playlist['usuario']['foto_perfil']}"

        for cancion in playlist['canciones']:
            cancion['portada_url'] = f"{settings.API_MEDIA_URL}{cancion['cancion']['portada']}"
            cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{cancion['cancion']['archivo_audio']}"
    
    
    
   
    return render(request, 'playlists/lista_playlist_completa.html', {'playlists_mostrar': playlists})



def lista_albumes_api(request):
    try:
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        response = requests.get(f"{settings.API_URL}albumes/", headers=headers)
        if response.status_code == 200:
            albumes = response.json()
            for album in albumes:
                album['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(album['portada']).path}"
                
                if 'canciones' in album:
                    for cancion in album['canciones']:
                        if 'portada' in cancion:
                            cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
                        if 'archivo_audio' in cancion:
                            cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"
        else:
            albumes = []
    except requests.exceptions.RequestException as e:
        albumes = []
        print(f"Error al obtener los álbumes: {e}")

    # Pasar los álbumes al template
    return render(request, 'albums/lista_albumes_completa.html', {'albumes_mostrar': albumes})

            
 
from urllib.parse import urlparse


def lista_albumes_usuario_api(request, nombre_usuario):
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    response = requests.get(f"{settings.API_URL}{nombre_usuario}/albumes", headers=headers)
    albumes = formato_respuesta(response)
    
    for album in albumes:
        album['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(album['portada']).path}"
        
        if 'canciones' in album:
            for cancion in album['canciones']:
                if 'portada' in cancion:
                    cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
                if 'archivo_audio' in cancion:
                    cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"

    return render(request, 'usuarios/lista_albumes_usuario.html', {
        'albumes_mostrar': albumes,
        'nombre_usuario': nombre_usuario
    })


def lista_usuarios_completa_api(request):
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[2]}'}
    url = f"{settings.API_URL}usuarios/lista_usuarios_completa/"    
    response = requests.get(url, headers=headers)
  
    if response.status_code == 200:
        usuarios = formato_respuesta(response)

        for usuario in usuarios:
            usuario['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(usuario['foto_perfil']).path}"
            
            for seguidor in usuario['seguidores']:
                seguidor['seguidor']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(seguidor['seguidor']['foto_perfil']).path}"
            
            for seguido in usuario['seguidos']:
                seguido['seguido']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(seguido['seguido']['foto_perfil']).path}"

        return render(request, 'usuarios/lista_usuarios_completa.html', {
            'usuarios_mostrar': usuarios
        })
    else:
        return render(request, 'usuarios/lista_usuarios_completa.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })
    

def lista_canciones_api(request):
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    url = f"{settings.API_URL}canciones/lista_canciones_completa/"    
    response = requests.get(url, headers=headers)
        
    if response.status_code == 200:
        canciones = formato_respuesta(response)

        for cancion in canciones:
            if 'portada' in cancion:
                cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
            if 'archivo_audio' in cancion:
                cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"
            
            # Obtener el conteo de likes como un número
            cancion['num_likes'] = len(cancion.get('likes', []))
        
        return render(request, 'canciones/lista_canciones_completa.html', {
            'canciones_mostrar': canciones,
        })
    else:
        return render(request, 'canciones/lista_canciones_completa.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })
   


def canciones_por_genero_api(request):
    headers = {'Authorization': f'Token {settings.AUTH_TOKEN}'}
    url = f"{settings.API_URL}canciones/generos/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        canciones = formato_respuesta(response)

        for cancion in canciones:
            if 'portada' in cancion:
                cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
            
            if 'archivo_audio' in cancion:
                cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"
            
            if 'usuario' in cancion:
                cancion['usuario']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['usuario']['foto_perfil']).path}"
                
        return render(request, 'canciones/canciones_genero.html', {
            'canciones': canciones,
            'api_media_url': settings.API_MEDIA_URL
        })
    else:
        return render(request, 'canciones/canciones_genero.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })

# BÚSQUEDAS AVANZADAS

def crear_cabecera():
    return {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}


def busqueda_usuarios_api(request):
    formulario = BusquedaUsuarioForm(request.GET)
    if formulario.is_valid():  
        headers = crear_cabecera()     
        response = requests.get(
            f"{settings.API_URL}usuarios/busqueda_simple",
            headers=headers,
            params={'textoBusqueda':formulario.data.get("textoBusqueda")}   
        )
        usuarios = formato_respuesta(response)

        for usuario in usuarios:
            usuario['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{usuario['foto_perfil']}"

        return render(request, "usuarios/lista_usuarios_completa.html", {"usuarios_mostrar": usuarios})
    
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    return redirect("index")




def usuario_busqueda_avanzada_api(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                f"{settings.API_URL}usuarios/busqueda_avanzada/",
                headers=headers,
                params=formulario.data
            )
            
            if response.status_code == requests.codes.ok:
                usuarios = formato_respuesta(response)

                if usuarios:
                    for usuario in usuarios:
                        usuario['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(usuario['foto_perfil']).path}"
                    
                    for seguidor in usuario['seguidores']:
                        seguidor['seguidor']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(seguidor['seguidor']['foto_perfil']).path}"
                    
                    for seguido in usuario['seguidos']:
                        seguido['seguido']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(seguido['seguido']['foto_perfil']).path}"

              
                return render(request, "usuarios/lista_usuarios_completa.html", {"usuarios_mostrar": usuarios})
            
            response.raise_for_status()
            
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'usuarios/busqueda_avanzada_usuarios.html', 
                            {"formulario": formulario, "errores": errores})
            else:
                return mi_error_500(request)
            
        except Exception as err:
            print(f'Error: {err}')
            return mi_error_500(request)
            
    formulario = BusquedaAvanzadaUsuarioForm(None)
    return render(request, 'usuarios/busqueda_avanzada_usuarios.html', {"formulario": formulario})





def album_busqueda_avanzada_api(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaAlbumForm(request.GET)

        
        try:
            headers = crear_cabecera()
            response = requests.get(
                f"{settings.API_URL}albumes/busqueda_avanzada/",
                headers=headers,
                params=formulario.data
            )
            print(f"Status: {response.status_code}")  # Añadir debug
            print(f"Response: {response.text}")   
            
            if response.status_code == requests.codes.ok:
                albumes = formato_respuesta(response)
    
                if albumes:
                    for album in albumes:
                        album['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(album['portada']).path}"
                        
                        # Procesar canciones si existen
                        if 'canciones' in album:
                            for cancion in album['canciones']:
                                if 'portada' in cancion:
                                    cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
                                if 'archivo_audio' in cancion:
                                    cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"

                return render(request, "albums/lista_albumes_completa.html", {"albumes_mostrar": albumes})

            
            response.raise_for_status()
            
        except HTTPError as http_err:
            print(f"HTTP Error: {http_err}")
            if response.status_code == 400:
                errores = formato_respuesta(response)
                
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'albums/busqueda_avanzada_albums.html', 
                            {"formulario": formulario, "errores": errores})
            return mi_error_500(request)
            
        except Exception as err:
            print(f'Error: {err}')
            return mi_error_500(request)
            
    formulario = BusquedaAvanzadaAlbumForm(None)
    return render(request, 'albums/busqueda_avanzada_albums.html', {"formulario": formulario})


def cancion_busqueda_avanzada_api(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaCancionForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                f"{settings.API_URL}canciones/busqueda_avanzada/",
                headers=headers,
                params=formulario.data
            )
            
            if response.status_code == requests.codes.ok:
                canciones = formato_respuesta(response)

                for cancion in canciones:
                    if 'portada' in cancion:
                        cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
                    if 'archivo_audio' in cancion:
                        cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"
                return render(request, "canciones/lista_canciones_completa.html", {"canciones_mostrar": canciones})
            
            response.raise_for_status()
            
        except HTTPError as http_err:
            print(f'error: {http_err}')
            if response.status_code == 400:
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'canciones/busqueda_avanzada_canciones.html', 
                            {"formulario": formulario, "errores": errores})
            return mi_error_500(request)
            
        except Exception as err:
            print(f'Error: {err}')
            return mi_error_500(request)
            
    formulario = BusquedaAvanzadaCancionForm(None)
    return render(request, 'canciones/busqueda_avanzada_canciones.html', {"formulario": formulario})


def playlist_busqueda_avanzada_api(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaPlaylistForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                f"{settings.API_URL}playlists/busqueda_avanzada/",
                headers=headers,
                params=formulario.data
            )
            
            if response.status_code == requests.codes.ok:
                playlists = formato_respuesta(response)
                
                for playlist in playlists:
                    playlist['usuario']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{playlist['usuario']['foto_perfil']}"

                    for cancion in playlist['canciones']:
                        cancion['portada_url'] = f"{settings.API_MEDIA_URL}{cancion['cancion']['portada']}"
                        cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{cancion['cancion']['archivo_audio']}"

                return render(request, "playlists/lista_playlist_completa.html", {"playlists_mostrar": playlists})
            
            response.raise_for_status()
            
        except HTTPError as http_err:
            if response.status_code == 400:
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'playlists/busqueda_avanzada_playlists.html', 
                            {"formulario": formulario, "errores": errores})
            return mi_error_500(request)
            
        except Exception as err:
            print(f'Error: {err}')
            return mi_error_500(request)
            
    formulario = BusquedaAvanzadaPlaylistForm(None)
    return render(request, 'playlists/busqueda_avanzada_playlists.html', {"formulario": formulario})


def crear_cabecera_contentType():
    return {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}', "Content-Type": "application/json"  }



#MÉTODOS CREAR


def usuario_crear(request):
    if request.method == "POST":
        try:
            formulario = UsuarioForm(request.POST, request.FILES)
            if not formulario.is_valid():
                return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})
                
            headers = helper.crear_cabecera_contentType()
            datos = formulario.cleaned_data.copy()
            
            if 'foto_perfil' in request.FILES:
                foto = request.FILES['foto_perfil']
                with foto.open('rb') as file:
                    foto_contenido = file.read()
                encoded = base64.b64encode(foto_contenido).decode('utf-8')
                datos['foto_perfil'] = f"data:{foto.content_type};base64,{encoded}"
            else:
                datos['foto_perfil'] = ''
            
            response = helper.realizar_peticion_crear(
                'usuarios/crear',
                datos
            )
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Usuario creado correctamente.')
                return redirect("lista_usuarios_completa")
            else:
                print(f"Error en usuario_crear - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en usuario_crear: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})
            return tratar_errores(request, response.status_code)
            
        except Exception as err:
            print(f"Error general en usuario_crear: {err}")
            return mi_error_500(request)
    else:
        formulario = UsuarioForm(None)
    return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})

def usuario_editar(request, id):
    if request.method == "POST":
        formulario = UsuarioUpdateForm(request.POST, request.FILES, initial={'id': id})
        if formulario.is_valid():
            headers = helper.crear_cabecera_contentType()
            datos = formulario.cleaned_data.copy()

            if not datos.get('password'):
                datos.pop('password', None)

            if 'foto_perfil' in request.FILES:
                foto = request.FILES['foto_perfil']
                with foto.open('rb') as file:
                    foto_contenido = file.read()
                encoded = base64.b64encode(foto_contenido).decode('utf-8')
                datos['foto_perfil'] = f"data:{foto.content_type};base64,{encoded}"
            else:
                datos.pop('foto_perfil', None)      
            
            response = helper.realizar_peticion_actualizar(
                f'usuarios/{id}/actualizar',
                datos
            )
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Usuario editado correctamente.')
                return redirect("lista_usuarios_completa")
            else:
                print(f"Error en usuario_editar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)
        else:
            print(f"Error de validación en usuario_editar: {formulario.errors}")
            for campo, errores in formulario.errors.items():
                for error in errores:
                    formulario.add_error(campo, error)

    else:
        try:
            usuario = helper.obtener_usuario(id)
            formulario = UsuarioUpdateForm(initial={
                'id': id,
                'nombre_usuario': usuario['nombre_usuario'],
                'email': usuario['email'],
                'bio': usuario.get('bio', ''),
                'foto_perfil': usuario.get('foto_perfil', '')
            })
        except Exception as err:
            print(f"Error al obtener usuario para editar: {err}")
            messages.error(request, 'Ocurrió un error al obtener los datos del usuario.')

    return render(request, 'usuarios/editar-usuario.html', {"formulario": formulario, "id": id})

def usuario_editar_nombre(request, usuario_id):
    try:
        usuario = helper.obtener_usuario(usuario_id)
        formulario = UsuarioActualizarNombreForm(request.POST or None, initial={'nombre_usuario': usuario['nombre_usuario']})
    except Exception as err:
        print(f"Error al obtener usuario para editar nombre: {err}")
        return mi_error_500(request)
    
    if request.method == "POST":
        try:
            if not formulario.is_valid():
                print(f"Error de validación en usuario_editar_nombre: {formulario.errors}")
                return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})

            response = helper.realizar_peticion_actualizar(
                f'usuarios/actualizar/nombre/{usuario_id}',
                request.POST.copy(),
                method='PATCH'
            )
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Nombre de usuario editado.')
                return redirect("lista_usuarios_completa")
            else:
                print(f"Error en usuario_editar_nombre - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en usuario_editar_nombre: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en usuario_editar_nombre: {err}")
            return mi_error_500(request)
    
    return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})

def usuario_eliminar(request, usuario_id):
    if request.method == "POST":
        try:
            response = helper.realizar_peticion_eliminar(f'usuarios/eliminar/{usuario_id}')
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Usuario eliminado correctamente.')
                return redirect("lista_usuarios_completa")
            else:
                print(f"Error en usuario_eliminar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en usuario_eliminar: {err}")
            return mi_error_500(request)
    else:
        try:
            usuario = helper.obtener_usuario(usuario_id)
            return render(request, 'usuarios/eliminar_confirmacion.html', {'usuario': usuario})
        except Exception as err:
            print(f"Error al obtener usuario para eliminar: {err}")
            return mi_error_500(request)



def album_crear(request):
    if request.method == 'POST':
        try:
            form = AlbumForm(request.POST, request.FILES)
            if not form.is_valid():
                print(f"Error de validación en album_crear: {form.errors}")
                return render(request, 'albums/album_crear.html', {'formulario': form})

            datos = form.cleaned_data.copy()
            
            if 'usuario' in datos:
                datos['usuario'] = int(datos['usuario'])

            headers = helper.crear_cabecera_contentType()

            if 'portada' in request.FILES:
                portada = request.FILES['portada']
                with portada.open('rb') as f:
                    portada_contenido = f.read()
                encoded = base64.b64encode(portada_contenido).decode('utf-8')
                datos['portada'] = f"data:{portada.content_type};base64,{encoded}"
            else:
                datos.pop('portada', None)

            response = helper.realizar_peticion_crear(
                'albumes/crear/',
                datos
            )

            if response.status_code in [200, 201]:
                messages.success(request, 'Álbum creado correctamente.')
                return redirect('lista_albumes')
            else:
                print(f"Error en album_crear - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en album_crear: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for campo, mensaje in errores.items():
                    form.add_error(campo, mensaje)
                return render(request, 'albums/album_crear.html', {'formulario': form})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en album_crear: {err}")
            return mi_error_500(request)
    else:
        form = AlbumForm()
    return render(request, 'albums/album_crear.html', {'formulario': form})

def album_editar(request, id):
    if request.method == 'POST':
        try:
            form = AlbumUpdateForm(request.POST, request.FILES)
            if not form.is_valid():
                print(f"Error de validación en album_editar: {form.errors}")
                return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})

            datos = form.cleaned_data.copy()
            album = helper.obtener_album(id)
            if album:
                datos['usuario'] = album['usuario']
            
            if 'portada' in request.FILES:
                portada = request.FILES['portada']
                with portada.open('rb') as f:
                    portada_contenido = f.read()
                encoded = base64.b64encode(portada_contenido).decode('utf-8')
                datos['portada'] = f"data:{portada.content_type};base64,{encoded}"
            else:
                datos.pop('portada', None)

            response = helper.realizar_peticion_actualizar(
                f'albumes/{id}/editar/',
                datos
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Álbum editado correctamente.')
                return redirect('lista_albumes')
            else:
                print(f"Error en album_editar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en album_editar: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for campo, mensaje in errores.items():
                    form.add_error(campo, mensaje)
                return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en album_editar: {err}")
            return mi_error_500(request)
    else:
        try:
            album = helper.obtener_album(id)
            form = AlbumUpdateForm(initial={
                'titulo': album.get('titulo', ''),
                'artista': album.get('artista', ''),
                'descripcion': album.get('descripcion', '')
            })
        except Exception as err:
            print(f"Error al obtener album para editar: {err}")
            return mi_error_500(request)
            
    return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})

def album_editar_titulo(request, id):
    try:
        album = helper.obtener_album(id)
        formulario = AlbumActualizarTituloForm(request.POST or None, initial={'titulo': album['titulo']})
    except Exception as err:
        print(f"Error al obtener album para editar título: {err}")
        return mi_error_500(request)
    
    if request.method == "POST":
        try:
            if not formulario.is_valid():
                print(f"Error de validación en album_editar_titulo: {formulario.errors}")
                return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})

            headers = helper.crear_cabecera_contentType()
            datos = request.POST.copy()
            response = helper.realizar_peticion_actualizar(
                f'albumes/actualizar/titulo/{id}/',
                datos,
                method='PATCH'
            )
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Título del álbum editado correctamente.')
                return redirect("lista_albumes")
            else:
                print(f"Error en album_editar_titulo - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en album_editar_titulo: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en album_editar_titulo: {err}")
            return mi_error_500(request)
    
    return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})

def album_eliminar(request, id):
    if request.method == "POST":
        try:
            response = helper.realizar_peticion_eliminar(f'albumes/{id}/eliminar/')
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Album eliminado correctamente.')
                return redirect("lista_albumes")
            else:
                print(f"Error en album_eliminar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en album_eliminar: {err}")
            return mi_error_500(request)
    else:
        try:
            album = helper.obtener_album(id)
            return render(request, 'albums/eliminar_album.html', {'album': album})
        except Exception as err:
            print(f"Error al obtener album para eliminar: {err}")
            return mi_error_500(request)
        

def playlist_crear(request):
    if request.method == 'POST':
        try:
            form = PlaylistForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en playlist_crear: {form.errors}")
                return render(request, 'playlists/crear_playlist.html', {'formulario': form})

            datos = form.cleaned_data.copy()
            datos['canciones'] = request.POST.getlist('canciones')

            response = helper.realizar_peticion_crear(
                'playlists/crear/',
                datos
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Playlist creada correctamente.')
                return redirect('lista_playlists')
            else:
                print(f"Error en playlist_crear - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en playlist_crear: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    form.add_error(error, errores[error])
                return render(request, 'playlists/crear_playlist.html', {'formulario': form})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en playlist_crear: {err}")
            return mi_error_500(request)
    else:
        form = PlaylistForm()
    return render(request, 'playlists/crear_playlist.html', {'formulario': form})

def playlist_editar(request, id):
    try:
        playlist = helper.obtener_playlist(id)
        if not playlist or 'error' in playlist:
            print(f"Error: No se encontró la playlist con id {id}")
            return redirect('lista_playlists')

 
        print("Playlist completa:", playlist)
        print("Canciones en playlist:", playlist.get('canciones', []))

    except Exception as e:
        print(f"Error al obtener playlist para editar: {e}")
        return redirect('lista_playlists')

    if request.method == 'POST':
        try:
            form = PlaylistUpdateForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en playlist_editar: {form.errors}")
                return render(request, 'playlists/editar_playlist.html', {'formulario': form, 'id': id})

            datos = form.cleaned_data.copy()
            datos['usuario'] = playlist.get('usuario')
            
            response = helper.realizar_peticion_actualizar(
                f'playlists/{id}/editar/',
                datos
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Playlist editada correctamente.')
                return redirect('lista_playlists')
            elif response.status_code == 400:
                errores = response.json()
                for campo, mensaje in errores.items():
                    form.add_error(campo, mensaje)
                return render(request, 'playlists/editar_playlist.html', {'formulario': form, 'id': id})
            else:
                print(f"Error en playlist_editar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en playlist_editar: {err}")
            return mi_error_500(request)
    else:
        # Extraemos los IDs correctamente dependiendo de la estructura
        canciones = playlist.get('canciones', [])
        print("Canciones antes de procesar:", canciones)
        
        canciones_seleccionadas = []
        for cancion in canciones:
            # Verificamos si la canción es un diccionario y tiene 'id'
            if isinstance(cancion, dict) and 'id' in cancion:
                canciones_seleccionadas.append(str(cancion['id']))
            # Si la canción es directamente el ID
            elif cancion is not None:
                canciones_seleccionadas.append(str(cancion))
        
        print("Canciones seleccionadas procesadas:", canciones_seleccionadas)
        
        # Creamos el formulario con los datos iniciales
        initial_data = {
            'nombre': playlist.get('nombre', ''),
            'descripcion': playlist.get('descripcion', ''),
            'publica': playlist.get('publica', False),
            'canciones': canciones_seleccionadas
        }
        
        print("Datos iniciales del formulario:", initial_data)
        form = PlaylistUpdateForm(initial=initial_data)

    return render(request, 'playlists/editar_playlist.html', {
        'formulario': form, 
        'id': id, 
        'playlist': playlist
    })

def playlist_editar_canciones(request, id):
    try:
        playlist = helper.obtener_playlist(id)
        print("Playlist recibida:", playlist)  # Debug
        
        if request.method == "POST":
            try:
                formulario = PlaylistActualizarCancionesForm(request.POST)
                if not formulario.is_valid():
                    return render(request, 'playlists/actualizar_canciones.html', {
                        "formulario": formulario,
                        "playlist": playlist,
                        'id': id
                    })

                datos = {
                    'canciones': request.POST.getlist('canciones')
                }
                
                response = helper.realizar_peticion_actualizar(
                    f'playlists/{id}/actualizar/canciones/',
                    datos,
                    method='PATCH'
                )
                
                if response.status_code == requests.codes.ok:
                    messages.success(request, 'Canciones de playlist editadas correctamente.')
                    return redirect("lista_playlists")
                elif response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        formulario.add_error(error, errores[error])
                    return render(request, 'playlists/actualizar_canciones.html', {
                        "formulario": formulario,
                        "playlist": playlist,
                        'id': id
                    })
                else:
                    print(f"Error en playlist_editar_canciones - Status: {response.status_code}")
                    return tratar_errores(request, response.status_code)

            except Exception as err:
                print(f"Error general en playlist_editar_canciones: {err}")
                return mi_error_500(request)
        else:
            # Debug de la estructura de las canciones
            canciones = playlist.get('canciones', [])
            print("Canciones de la playlist:", canciones)
            
            canciones_seleccionadas = []
            for cancion in canciones:
                if isinstance(cancion, dict) and 'id' in cancion:
                    canciones_seleccionadas.append(str(cancion['id']))
                elif cancion is not None:
                    canciones_seleccionadas.append(str(cancion))
            
            print("Canciones procesadas:", canciones_seleccionadas)
            
            initial_data = {
                'canciones': canciones_seleccionadas
            }
            formulario = PlaylistActualizarCancionesForm(initial=initial_data)
        
        return render(request, 'playlists/actualizar_canciones.html', {
            "formulario": formulario,
            "playlist": playlist,
            'id': id
        })
    except Exception as err:
        print(f"Error al obtener playlist para editar canciones: {err}")
        return mi_error_500(request)

def playlist_eliminar(request, id):
    if request.method == "POST":
        try:
            response = helper.realizar_peticion_eliminar(f'playlists/{id}/eliminar/')
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Playlist eliminada correctamente.')
                return redirect("lista_playlists")
            else:
                print(f"Error en playlist_eliminar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en playlist_eliminar: {err}")
            return mi_error_500(request)
    else:
        try:
            playlist = helper.obtener_playlist(id)
            return render(request, 'playlists/eliminar_playlist.html', {'playlist': playlist})
        except Exception as err:
            print(f"Error al obtener playlist para eliminar: {err}")
            return mi_error_500(request)
        
def like_crear(request):
    if request.method == 'POST':
        try:
            form = LikeForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en like_crear: {form.errors}")
                return render(request, 'likes/crear_like.html', {'formulario': form})

            datos = form.cleaned_data.copy()
            
            response = helper.realizar_peticion_crear(
                'likes/crear/',
                datos
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Like creado correctamente.')
                return redirect('lista_canciones')
            else:
                print(f"Error en like_crear - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en like_crear: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for campo, mensaje in errores.items():
                    form.add_error(campo, mensaje)
                return render(request, 'likes/crear_like.html', {'formulario': form})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en like_crear: {err}")
            return mi_error_500(request)
    else:
        form = LikeForm()
    return render(request, 'likes/crear_like.html', {'formulario': form})
        
def like_eliminar(request):
    if request.method == 'POST':
        try:
            form = LikeDeleteForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en like_eliminar: {form.errors}")
                return render(request, 'likes/eliminar_like.html', {'formulario': form})

            datos = form.cleaned_data.copy()
            
            response = requests.delete(
                f'{settings.API_URL}likes/eliminar/',
                headers=crear_cabecera_contentType(),
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Like eliminado correctamente.')
                return redirect('lista_canciones')
            else:
                print(f"Error en like_eliminar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en like_eliminar: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                if isinstance(errores, dict):
                    for campo, mensaje in errores.items():
                        form.add_error(campo, mensaje)
                return render(request, 'likes/eliminar_like.html', {'formulario': form})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en like_eliminar: {err}")
            return mi_error_500(request)
    else:
        form = LikeDeleteForm()
        
    return render(request, 'likes/eliminar_like.html', {'formulario': form})




# def usuario_crear(request):
#     if request.method == "POST":
#         try:
#             formulario = UsuarioForm(request.POST, request.FILES)
#             if not formulario.is_valid():
#                 return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})
                
#             headers = crear_cabecera_contentType()
#             datos = formulario.cleaned_data.copy()
            
#             if 'foto_perfil' in request.FILES:
#                 foto = request.FILES['foto_perfil']
#                 with foto.open('rb') as file:
#                     foto_contenido = file.read()
#                 encoded = base64.b64encode(foto_contenido).decode('utf-8')
#                 datos['foto_perfil'] = f"data:{foto.content_type};base64,{encoded}"
#             else:
#                 datos['foto_perfil'] = ''
            
#             response = requests.post(
#                 f'{settings.API_URL}usuarios/crear',
#                 headers=headers,
#                 data=json.dumps(datos)
#             )
            
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Usuario creado correctamente.')
#                 return redirect("lista_usuarios_completa")
#             else:
#                 print(f"Error en usuario_crear - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en usuario_crear: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for error in errores:
#                     formulario.add_error(error, errores[error])
#                 return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})
#             return tratar_errores(request, response.status_code)
            
#         except Exception as err:
#             print(f"Error general en usuario_crear: {err}")
#             return mi_error_500(request)
#     else:
#         formulario = UsuarioForm(None)
#     return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})

# def album_crear(request):
#     if request.method == 'POST':
#         try:
#             form = AlbumForm(request.POST, request.FILES)
#             if not form.is_valid():
#                 print(f"Error de validación en album_crear: {form.errors}")
#                 return render(request, 'albums/album_crear.html', {'formulario': form})

#             datos = form.cleaned_data.copy()
            
#             if 'usuario' in datos:
#                 datos['usuario'] = int(datos['usuario'])

#             headers = crear_cabecera_contentType()

#             if 'portada' in request.FILES:
#                 portada = request.FILES['portada']
#                 with portada.open('rb') as f:
#                     portada_contenido = f.read()
#                 encoded = base64.b64encode(portada_contenido).decode('utf-8')
#                 datos['portada'] = f"data:{portada.content_type};base64,{encoded}"
#             else:
#                 datos.pop('portada', None)

#             response = requests.post(
#                 f'{settings.API_URL}albumes/crear/', 
#                 headers=headers, 
#                 json=datos
#             )

#             if response.status_code in [200, 201]:
#                 messages.success(request, 'Álbum creado correctamente.')
#                 return redirect('lista_albumes')
#             else:
#                 print(f"Error en album_crear - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en album_crear: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for campo, mensaje in errores.items():
#                     form.add_error(campo, mensaje)
#                 return render(request, 'albums/album_crear.html', {'formulario': form})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en album_crear: {err}")
#             return mi_error_500(request)
#     else:
#         form = AlbumForm()
#     return render(request, 'albums/album_crear.html', {'formulario': form})

# def playlist_crear(request):
#     if request.method == 'POST':
#         try:
#             form = PlaylistForm(request.POST)
#             if not form.is_valid():
#                 print(f"Error de validación en playlist_crear: {form.errors}")
#                 return render(request, 'playlists/crear_playlist.html', {'formulario': form})

#             datos = form.cleaned_data.copy()
#             datos['canciones'] = request.POST.getlist('canciones')

#             response = requests.post(
#                 f'{settings.API_URL}playlists/crear/',
#                 headers=crear_cabecera_contentType(),
#                 data=json.dumps(datos)
#             )

#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Playlist creada correctamente.')
#                 return redirect('lista_playlists')
#             else:
#                 print(f"Error en playlist_crear - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en playlist_crear: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for error in errores:
#                     form.add_error(error, errores[error])
#                 return render(request, 'playlists/crear_playlist.html', {'formulario': form})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en playlist_crear: {err}")
#             return mi_error_500(request)
#     else:
#         form = PlaylistForm()
#     return render(request, 'playlists/crear_playlist.html', {'formulario': form})

# def like_crear(request):
#     if request.method == 'POST':
#         try:
#             form = LikeForm(request.POST)
#             if not form.is_valid():
#                 print(f"Error de validación en like_crear: {form.errors}")
#                 return render(request, 'likes/crear_like.html', {'formulario': form})

#             datos = form.cleaned_data.copy()
            
#             response = requests.post(
#                 f'{settings.API_URL}likes/crear/',
#                 headers=crear_cabecera_contentType(),
#                 data=json.dumps(datos)
#             )

#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Like creado correctamente.')
#                 return redirect('lista_canciones')
#             else:
#                 print(f"Error en like_crear - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en like_crear: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for campo, mensaje in errores.items():
#                     form.add_error(campo, mensaje)
#                 return render(request, 'likes/crear_like.html', {'formulario': form})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en like_crear: {err}")
#             return mi_error_500(request)
#     else:
#         form = LikeForm()
#     return render(request, 'likes/crear_like.html', {'formulario': form})




# MÉTODOS EDITAR

# def usuario_editar(request, id):
#     if request.method == "POST":
#         try:
#             formulario = UsuarioUpdateForm(request.POST, request.FILES)
#             if not formulario.is_valid():
#                 print(f"Error de validación en usuario_editar: {formulario.errors}")
#                 return render(request, 'usuarios/editar-usuario.html', 
#                             {"formulario": formulario, "id": id})
                
#             headers = crear_cabecera_contentType()
#             datos = formulario.cleaned_data.copy()

#             if not datos.get('password'):
#                 datos.pop('password', None)

       
#             if 'foto_perfil' in request.FILES:
#                 foto = request.FILES['foto_perfil']
#                 with foto.open('rb') as file:
#                     foto_contenido = file.read()
#                 encoded = base64.b64encode(foto_contenido).decode('utf-8')
#                 datos['foto_perfil'] = f"data:{foto.content_type};base64,{encoded}"
#             else:
#                 datos.pop('foto_perfil', None)      
            
#             response = requests.put(
#                 f'{settings.API_URL}usuarios/{id}/actualizar',
#                 headers=headers,
#                 data=json.dumps(datos)
#             )
            
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Usuario editado correctamente.')
#                 return redirect("lista_usuarios_completa")
#             else:
#                 print(f"Error en usuario_editar - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en usuario_editar: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for error in errores:
#                     formulario.add_error(error, errores[error])
#                 return render(request, 'usuarios/editar-usuario.html', 
#                             {"formulario": formulario, "id": id})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en usuario_editar: {err}")
#             return mi_error_500(request)

#     else:
#         try:
#             usuario = helper.obtener_usuario(id)
#             formulario = UsuarioForm(initial={
#                 'nombre_usuario': usuario['nombre_usuario'],
#                 'email': usuario['email'],
#                 'bio': usuario.get('bio', ''),
#                 'foto_perfil': usuario.get('foto_perfil', '')
#             })
#         except Exception as err:
#             print(f"Error al obtener usuario para editar: {err}")
#             return mi_error_500(request)

#     return render(request, 'usuarios/editar-usuario.html', {"formulario": formulario, "id": id})

# def usuario_editar_nombre(request, usuario_id):
#     try:
#         usuario = helper.obtener_usuario(usuario_id)
#         formulario = UsuarioActualizarNombreForm(request.POST or None, initial={'nombre_usuario': usuario['nombre_usuario']})
#     except Exception as err:
#         print(f"Error al obtener usuario para editar nombre: {err}")
#         return mi_error_500(request)
    
#     if request.method == "POST":
#         try:
#             if not formulario.is_valid():
#                 print(f"Error de validación en usuario_editar_nombre: {formulario.errors}")
#                 return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})

#             headers = crear_cabecera_contentType()
#             datos = request.POST.copy()
#             response = requests.patch(
#                 f'{settings.API_URL}usuarios/actualizar/nombre/{usuario_id}',
#                 headers=headers,
#                 data=json.dumps(datos)
#             )
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Nombre de usuario editado.')
#                 return redirect("lista_usuarios_completa")
#             else:
#                 print(f"Error en usuario_editar_nombre - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en usuario_editar_nombre: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for error in errores:
#                     formulario.add_error(error, errores[error])
#                 return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en usuario_editar_nombre: {err}")
#             return mi_error_500(request)
    
#     return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})

# def album_editar(request, id):
#     if request.method == 'POST':
#         try:
#             form = AlbumUpdateForm(request.POST, request.FILES)
#             if not form.is_valid():
#                 print(f"Error de validación en album_editar: {form.errors}")
#                 return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})

#             datos = form.cleaned_data.copy()
#             album = helper.obtener_album(id)
#             if album:
#                 datos['usuario'] = album['usuario']
            
#             headers = crear_cabecera_contentType()

#             if 'portada' in request.FILES:
#                 portada = request.FILES['portada']
#                 with portada.open('rb') as f:
#                     portada_contenido = f.read()
#                 encoded = base64.b64encode(portada_contenido).decode('utf-8')
#                 datos['portada'] = f"data:{portada.content_type};base64,{encoded}"
#             else:
#                 datos.pop('portada', None)

#             response = requests.put(
#                 f'{settings.API_URL}albumes/{id}/editar/', 
#                 headers=headers, 
#                 json=datos
#             )

#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Álbum editado correctamente.')
#                 return redirect('lista_albumes')
#             else:
#                 print(f"Error en album_editar - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en album_editar: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for campo, mensaje in errores.items():
#                     form.add_error(campo, mensaje)
#                 return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en album_editar: {err}")
#             return mi_error_500(request)
#     else:
#         try:
#             album = helper.obtener_album(id)
#             form = AlbumUpdateForm(initial={
#                 'titulo': album.get('titulo', ''),
#                 'artista': album.get('artista', ''),
#                 'descripcion': album.get('descripcion', '')
#             })
#         except Exception as err:
#             print(f"Error al obtener album para editar: {err}")
#             return mi_error_500(request)
            
#     return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})

# def album_editar_titulo(request, id):
#     try:
#         album = helper.obtener_album(id)
#         formulario = AlbumActualizarTituloForm(request.POST or None, initial={'titulo': album['titulo']})
#     except Exception as err:
#         print(f"Error al obtener album para editar título: {err}")
#         return mi_error_500(request)
    
#     if request.method == "POST":
#         try:
#             if not formulario.is_valid():
#                 print(f"Error de validación en album_editar_titulo: {formulario.errors}")
#                 return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})

#             headers = crear_cabecera_contentType()
#             datos = request.POST.copy()
#             response = requests.patch(
#                 f'{settings.API_URL}albumes/actualizar/titulo/{id}/',
#                 headers=headers,
#                 data=json.dumps(datos)
#             )
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Título del álbum editado correctamente.')
#                 return redirect("lista_albumes")
#             else:
#                 print(f"Error en album_editar_titulo - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en album_editar_titulo: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for error in errores:
#                     formulario.add_error(error, errores[error])
#                 return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en album_editar_titulo: {err}")
#             return mi_error_500(request)
    
#     return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})

# def playlist_editar(request, id):
#     try:
#         playlist = helper.obtener_playlist(id)
#         if not playlist or 'error' in playlist:
#             print(f"Error: No se encontró la playlist con id {id}")
#             return redirect('lista_playlists')

#         usuario_id = playlist.get('usuario')
#     except Exception as e:
#         print(f"Error al obtener playlist para editar: {e}")
#         return redirect('lista_playlists')

#     if request.method == 'POST':
#         try:
#             form = PlaylistUpdateForm(request.POST)
#             if not form.is_valid():
#                 print(f"Error de validación en playlist_editar: {form.errors}")
#                 return render(request, 'playlists/editar_playlist.html', {'formulario': form, 'id': id})

#             datos = form.cleaned_data.copy()
#             datos['usuario'] = usuario_id
#             headers = crear_cabecera_contentType()

#             response = requests.put(
#                 f'{settings.API_URL}playlists/{id}/editar/', 
#                 headers=headers, 
#                 json=datos
#             )

#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Playlist editada correctamente.')
#                 return redirect('lista_playlists')
#             else:
#                 print(f"Error en playlist_editar - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except HTTPError as http_err:
#             print(f"Error HTTP en playlist_editar: {http_err}")
#             if response.status_code == 400:
#                 errores = response.json()
#                 for campo, mensaje in errores.items():
#                     form.add_error(campo, mensaje)
#                 return render(request, 'playlists/editar_playlist.html', {'formulario': form, 'id': id})
#             return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en playlist_editar: {err}")
#             return mi_error_500(request)
#     else:
#         canciones_ids = [cancion.get('id') for cancion in playlist.get('canciones', [])]
#         form = PlaylistUpdateForm(initial={
#             'nombre': playlist.get('nombre', ''),
#             'descripcion': playlist.get('descripcion', ''),
#             'canciones': canciones_ids,
#             'publica': playlist.get('publica', False)
#         })

#     return render(request, 'playlists/editar_playlist.html', {'formulario': form, 'id': id})

# def playlist_editar_canciones(request, id):
#     try:
#         playlist = helper.obtener_playlist(id)
#         if request.method == "POST":
#             try:
#                 formulario = PlaylistActualizarCancionesForm(request.POST)
#                 if not formulario.is_valid():
#                     print(f"Error de validación en playlist_editar_canciones: {formulario.errors}")
#                     return render(request, 'playlists/actualizar_canciones.html', {
#                         "formulario": formulario,
#                         "playlist": playlist,
#                         'id': id
#                     })

#                 headers = crear_cabecera_contentType()
#                 datos = {
#                     'canciones': request.POST.getlist('canciones')
#                 }
                
#                 response = requests.patch(
#                     f'{settings.API_URL}playlists/{id}/actualizar/canciones/',
#                     headers=headers,
#                     data=json.dumps(datos)
#                 )
#                 if response.status_code == requests.codes.ok:
#                     messages.success(request, 'Canciones de playlist editadas correctamente.')
#                     return redirect("lista_playlists")
#                 else:
#                     print(f"Error en playlist_editar_canciones - Status: {response.status_code}")
#                     return tratar_errores(request, response.status_code)

#             except HTTPError as http_err:
#                 print(f"Error HTTP en playlist_editar_canciones: {http_err}")
#                 if response.status_code == 400:
#                     errores = response.json()
#                     for error in errores:
#                         formulario.add_error(error, errores[error])
#                     return render(request, 'playlists/actualizar_canciones.html', {
#                         "formulario": formulario,
#                         "playlist": playlist,
#                         'id': id
#                     })
#                 return tratar_errores(request, response.status_code)

#             except Exception as err:
#                 print(f"Error general en playlist_editar_canciones: {err}")
#                 return mi_error_500(request)
#         else:
#             canciones_seleccionadas = [cancion.get('id') for cancion in playlist.get('canciones', [])]
#             formulario = PlaylistActualizarCancionesForm(initial={
#                 'canciones': canciones_seleccionadas
#             })
        
#         return render(request, 'playlists/actualizar_canciones.html', {
#             "formulario": formulario,
#             "playlist": playlist,
#             'id': id
#         })
#     except Exception as err:
#         print(f"Error al obtener playlist para editar canciones: {err}")
#         return mi_error_500(request)
    

# MÉTODOS ELIMINAR
# def usuario_eliminar(request, usuario_id):
#     if request.method == "POST":
#         try:
#             headers = crear_cabecera()
#             response = requests.delete(
#                 f'{settings.API_URL}usuarios/eliminar/{usuario_id}',
#                 headers=headers,
#             )
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Usuario eliminado correctamente.')
#                 return redirect("lista_usuarios_completa")
#             else:
#                 print(f"Error en usuario_eliminar - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en usuario_eliminar: {err}")
#             return mi_error_500(request)
#     else:
#         try:
#             usuario = helper.obtener_usuario(usuario_id)
#             return render(request, 'usuarios/eliminar_confirmacion.html', {'usuario': usuario})
#         except Exception as err:
#             print(f"Error al obtener usuario para eliminar: {err}")
#             return mi_error_500(request)

# def album_eliminar(request, id):
#     if request.method == "POST":
#         try:
#             headers = crear_cabecera()
#             response = requests.delete(
#                 f'{settings.API_URL}albumes/{id}/eliminar/',
#                 headers=headers,
#             )
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Album eliminado correctamente.')
#                 return redirect("lista_albumes")
#             else:
#                 print(f"Error en album_eliminar - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en album_eliminar: {err}")
#             return mi_error_500(request)
#     else:
#         try:
#             album = helper.obtener_album(id)
#             return render(request, 'albums/eliminar_album.html', {'album': album})
#         except Exception as err:
#             print(f"Error al obtener album para eliminar: {err}")
#             return mi_error_500(request)

# def playlist_eliminar(request, id):
#     if request.method == "POST":
#         try:
#             headers = crear_cabecera_contentType()
#             response = requests.delete(
#                 f'{settings.API_URL}playlists/{id}/eliminar/',
#                 headers=headers,
#             )
#             if response.status_code == requests.codes.ok:
#                 messages.success(request, 'Playlist eliminada correctamente.')
#                 return redirect("lista_playlists")
#             else:
#                 print(f"Error en playlist_eliminar - Status: {response.status_code}")
#                 return tratar_errores(request, response.status_code)

#         except Exception as err:
#             print(f"Error general en playlist_eliminar: {err}")
#             return mi_error_500(request)
#     else:
#         try:
#             playlist = helper.obtener_playlist(id)
#             return render(request, 'playlists/eliminar_playlist.html', {'playlist': playlist})
#         except Exception as err:
#             print(f"Error al obtener playlist para eliminar: {err}")
#             return mi_error_500(request)
        


























def cancion_playlist_crear(request):
    if request.method == 'POST':
        try:
            form = CancionPlaylistForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en cancion_playlist_crear: {form.errors}")
                return render(request, 'cancion_playlist/crear.html', {'formulario': form})

            headers = crear_cabecera_contentType()
            datos = {
                'playlist': form.cleaned_data['playlist'],
                'canciones': form.cleaned_data['canciones']
            }
            
            response = requests.post(
                f'{settings.API_URL}cancion-playlist/crear/',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Playlist con canciones creada correctamente.')
                return redirect('lista_playlists')
            else:
                print(f"Error en cancion_playlist_crear - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en cancion_playlist_crear: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                if isinstance(errores, dict):
                    for campo, mensaje in errores.items():
                        form.add_error(None, mensaje)
                return render(request, 'cancion_playlist/crear.html', {'formulario': form})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en cancion_playlist_crear: {err}")
            return mi_error_500(request)
    else:
        form = CancionPlaylistForm()
        
    return render(request, 'cancion_playlist/crear.html', {'formulario': form})

def cancion_playlist_editar(request, id):
    try:
        playlist = helper.obtener_playlist(id)
        canciones_actuales = [cancion.get('id') for cancion in playlist.get('canciones', [])]
    except Exception as err:
        print(f"Error al obtener playlist para editar canciones: {err}")
        return mi_error_500(request)
    
    if request.method == 'POST':
        try:
            form = CancionPlaylistForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en cancion_playlist_editar: {form.errors}")
                return render(request, 'cancion_playlist/editar.html', {
                    'formulario': form,
                    'playlist': playlist,
                    'id': id
                })

            headers = crear_cabecera_contentType()
            datos = {
                'playlist': id,
                'canciones': form.cleaned_data['canciones']
            }
            
            response = requests.put(
                f'{settings.API_URL}playlists/{id}/actualizar/canciones/',
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Playlist con canciones editada correctamente.')
                return redirect('lista_playlists')
            else:
                print(f"Error en cancion_playlist_editar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en cancion_playlist_editar: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                if isinstance(errores, dict):
                    for campo, mensaje in errores.items():
                        form.add_error(None, mensaje)
                return render(request, 'cancion_playlist/editar.html', {
                    'formulario': form,
                    'playlist': playlist,
                    'id': id
                })
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en cancion_playlist_editar: {err}")
            return mi_error_500(request)
    else:
        initial_data = {
            'playlist': str(id),
            'canciones': canciones_actuales
        }
        form = CancionPlaylistForm(initial=initial_data)
        form.fields['playlist'].widget.attrs['disabled'] = True
        
    return render(request, 'cancion_playlist/editar.html', {
        'formulario': form,
        'playlist': playlist,
        'id': id
    })



def detalle_album_crear(request):
    if request.method == 'POST':
        try:
            form = DetalleAlbumForm(request.POST)
            if not form.is_valid():
                print(f"Error de validación en detalle_album_crear: {form.errors}")
                return render(request, 'detalles_album/detalle_album_crear.html', {'formulario': form})

            data = form.cleaned_data
            album_id = data.pop('album')
            print(f"Procesando creación de detalle para álbum ID: {album_id}")

            headers = crear_cabecera_contentType()
            response = requests.post(
                f'{settings.API_URL}albumes/{album_id}/detalles/',
                json=data, 
                headers=headers
            )

            if response.status_code == requests.codes.ok:
                messages.success(request, 'Detalle del álbum creado correctamente.')
                return redirect('lista_albumes')
            else:
                print(f"Error en detalle_album_crear - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en detalle_album_crear: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for campo, mensaje in errores.items():
                    form.add_error(campo, mensaje)
                return render(request, 'detalles_album/detalle_album_crear.html', {'formulario': form})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en detalle_album_crear: {err}")
            return mi_error_500(request)
    else:
        form = DetalleAlbumForm()

    return render(request, 'detalles_album/detalle_album_crear.html', {'formulario': form})

def detalle_album_editar(request, id):
    if request.method == "POST":
        try:
            formulario = DetalleAlbumForm(request.POST)
            if not formulario.is_valid():
                print(f"Error de validación en detalle_album_editar: {formulario.errors}")
                return render(request, 'detalles_album/detalle_album_actualizar.html', 
                            {"formulario": formulario, "id": id})
                
            headers = crear_cabecera_contentType()
            data = formulario.cleaned_data.copy()
            
            response = requests.put(
                f'{settings.API_URL}albumes/detalles/{id}/editar/',
                headers=headers,
                json=data
            )
            
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Detalle del álbum editado correctamente.')
                return redirect("lista_albumes")
            else:
                print(f"Error en detalle_album_editar - Status: {response.status_code}")
                return tratar_errores(request, response.status_code)

        except HTTPError as http_err:
            print(f"Error HTTP en detalle_album_editar: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'detalles_album/detalle_album_actualizar.html', 
                            {"formulario": formulario, "id": id})
            return tratar_errores(request, response.status_code)

        except Exception as err:
            print(f"Error general en detalle_album_editar: {err}")
            return mi_error_500(request)
    else:
        try:
            detalle = helper.obtener_detalle_album(id)
            formulario = DetalleAlbumForm(initial={
                'productor': detalle.get('productor', ''),
                'estudio_grabacion': detalle.get('estudio_grabacion', ''),
                'numero_pistas': detalle.get('numero_pistas', 0),
                'sello_discografico': detalle.get('sello_discografico', ''),
                'album': detalle.get('album', '')
            })
            print(f"Detalle del álbum ID {id} obtenido correctamente")
            
        except Exception as err:
            print(f"Error al obtener detalle del álbum {id}: {err}")
            return mi_error_500(request)

    return render(request, 'detalles_album/detalle_album_actualizar.html', 
                {"formulario": formulario, "id": id})






def tratar_errores(request,codigo):
    if codigo == 404:
        return mi_error_404(request)
    else:
        return mi_error_500(request)
        


#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)








 

   
