from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .forms import BusquedaUsuarioForm



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

    
    return render(request, 'playlists/lista_playlists.html', {'playlists': playlists})

            
 
def lista_albumes_usuario_api(request, nombre_usuario):

    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    response = requests.get(f"{settings.API_BASE_URL}{nombre_usuario}/albumes", headers=headers)
    albumes = response.json()
    for album in albumes:
           
            album['portada_url'] = f"{settings.API_MEDIA_URL}{album['portada']}"

            if 'canciones' in album:
                for cancion in album['canciones']:
                    if 'portada' in cancion:
                        cancion['portada_url'] = f"{settings.API_MEDIA_URL}{cancion['portada']}"
                    if 'archivo_audio' in cancion:
                        cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{cancion['archivo_audio']}"


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

        print(f'{usuarios}')
        for usuario in usuarios:
            
            usuario['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{usuario['foto_perfil']}"

            for seguidor in usuario['seguidores']:
                    seguidor['seguidor']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{seguidor['seguidor']['foto_perfil']}"
            
            for seguido in usuario['seguidos']:
                    seguido['seguido']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{seguido['seguido']['foto_perfil']}"

        

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
                cancion['portada_url'] = f"{settings.API_MEDIA_URL}{cancion['portada']}"
            if 'archivo_audio' in cancion:
                cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{cancion['archivo_audio']}"
        
        
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
    
    print(f"Haciendo petición a: {url}")  # Debug URL
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        canciones = response.json()
        print(f'{canciones}')

        for cancion in canciones:
            if 'portada' in cancion:
                cancion['portada_url'] = f"{settings.API_MEDIA_URL}{cancion['portada']}"
            
            if 'archivo_audio' in cancion:
                cancion['archivo_audio_url'] = f"{settings.API_MEDIA_URL}{cancion['archivo_audio']}"

            
            if 'usuario' in cancion:
                cancion['usuario']['foto_perfil_url'] = f"{settings.API_MEDIA_URL}{cancion['usuario']['foto_perfil']}" 
            
                
                
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
            f"{settings.API_BASE_URL}usuarios/busqueda_simple/",
            headers=headers,
            params=formulario.cleaned_data    
        )

        
        usuarios = response.json()
        return render(request, "usuarios/busqueda_usuarios.html", {"usuarios_mostrar": usuarios})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META("HTTP_REFERER"))
    else:
        return redirect("index")
 

   
