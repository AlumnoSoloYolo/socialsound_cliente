from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .forms import *
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
import base64
import datetime
import json


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

def usuario_crear(request):
    if (request.method == "POST"):
        try:
            formulario = UsuarioForm(request.POST, request.FILES)
            if not formulario.is_valid():
                return render(request, 'usuarios/crear-usuario.html', {"formulario": formulario})
                
            headers = crear_cabecera_contentType()
            datos = formulario.cleaned_data.copy()
            
            if 'foto_perfil' in request.FILES:
                    foto = request.FILES['foto_perfil']
                    # Leemos todo el contenido del archivo
                    with foto.open('rb') as f:
                        foto_contenido = f.read()
                        
                    # Imprimimos el tamaño para debug
                    print(f"Tamaño de la foto: {len(foto_contenido)} bytes")
                    
                    # Codificamos a base64 incluyendo el tipo MIME
                    encoded = base64.b64encode(foto_contenido).decode('utf-8')
                    datos['foto_perfil'] = f"data:{foto.content_type};base64,{encoded}"
                    
                    # Imprimimos el tamaño del base64 para debug
                    print(f"Tamaño del base64: {len(encoded)} caracteres")
            else:
                    datos['foto_perfil'] = ''

            print("Datos que se envían al backend:", datos)
            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/usuarios/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("lista_usuarios_completa")
            else:
                print("Respuesta del backend:", response.text)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 
                            'usuarios/crear-usuarios.html',
                            {"formulario": formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = UsuarioForm(None)
    return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})




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




 

   
