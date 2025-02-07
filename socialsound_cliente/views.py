from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .forms import *
from requests.exceptions import HTTPError



def index(request):
    return render(request, "index.html");

def lista_playlists_api(request): 
  
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    response = requests.get(f"{settings.API_BASE_URL}playlists", headers=headers)
    playlists = response.json()
    # print(f'{playlists}')
    for playlist in playlists:

        playlist['usuario']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{playlist['usuario']['foto_perfil']}"

        for cancion in playlist['canciones']:
            cancion['portada_url'] = f"{settings.API_MEDIA_URL}{cancion['cancion']['portada']}"
            cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{cancion['cancion']['archivo_audio']}"
    
            print(f'{cancion['cancion']['archivo_audio']}')
            print(f'{cancion['portada_url']}')

    
   
    return render(request, 'playlists/lista_playlists.html', {'playlists': playlists})

            
 
from urllib.parse import urlparse

from urllib.parse import urlparse

def lista_albumes_usuario_api(request, nombre_usuario):
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    response = requests.get(f"{settings.API_BASE_URL}{nombre_usuario}/albumes", headers=headers)
    albumes = response.json()
    
    for album in albumes:
        album['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(album['portada']).path}"
        
        if 'canciones' in album:
            for cancion in album['canciones']:
                if 'portada' in cancion:
                    cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
                if 'archivo_audio' in cancion:
                    cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"

    return render(request, 'usuarios/lista_albumes_usuario.html', {
        'lista_albumes': albumes,
        'nombre_usuario': nombre_usuario
    })


def lista_usuarios_completa_api(request):
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    url = f"{settings.API_BASE_URL}usuarios/lista_usuarios_completa/"    
    response = requests.get(url, headers=headers)
  
    if response.status_code == 200:
        usuarios = response.json()

        for usuario in usuarios:
            usuario['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(usuario['foto_perfil']).path}"
            
            for seguidor in usuario['seguidores']:
                seguidor['seguidor']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(seguidor['seguidor']['foto_perfil']).path}"
            
            for seguido in usuario['seguidos']:
                seguido['seguido']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{urlparse(seguido['seguido']['foto_perfil']).path}"

        return render(request, 'usuarios/lista_usuarios_completa.html', {
            'usuarios': usuarios
        })
    else:
        return render(request, 'usuarios/lista_usuarios_completa.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })
    

def lista_canciones_api(request):
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    url = f"{settings.API_BASE_URL}canciones/lista_canciones_completa/"    
    response = requests.get(url, headers=headers)
        
    if response.status_code == 200:
        canciones = response.json()

        for cancion in canciones:
            if 'portada' in cancion:
                cancion['portada_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['portada']).path}"
            if 'archivo_audio' in cancion:
                cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{urlparse(cancion['archivo_audio']).path}"
        
        return render(request, 'canciones/lista_canciones_completa.html', {
            'canciones': canciones,
            'api_media_url': settings.API_MEDIA_URL
        })
    else:
        return render(request, 'canciones/lista_canciones_completa.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })


def canciones_por_genero_api(request):
    headers = {'Authorization': f'Token {settings.AUTH_TOKEN}'}
    url = f"{settings.API_BASE_URL}canciones/generos/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        canciones = response.json()

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
            f"{settings.API_BASE_URL}usuarios/busqueda_simple",
            headers=headers,
            params={'textoBusqueda':formulario.data.get("textoBusqueda")}   
        )
        usuarios = response.json()

        for usuario in usuarios:
            usuario['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{usuario['foto_perfil']}"

        return render(request, "usuarios/lista_usuarios.html", {"usuarios_mostrar": usuarios})
    
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    return redirect("index")




def usuario_busqueda_avanzada_api(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/usuarios/busqueda_avanzada/',
                headers=headers,
                params=formulario.data
            )
            
            if response.status_code == requests.codes.ok:
                usuarios = response.json()
                print(f'{usuarios}')
                return render(request, "usuarios/lista_usuarios.html", {"usuarios_mostrar": usuarios})
            
            response.raise_for_status()
            
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
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
 

   
