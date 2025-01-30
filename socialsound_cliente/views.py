from django.shortcuts import render
import requests
from django.conf import settings



def lista_playlists_api(request): ### rol cliente
  
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[2]}'}
    response = requests.get(f"{settings.API_BASE_URL}playlists", headers=headers)
    playlists = response.json()
    return render(request, 'playlists/lista_playlists.html', {'playlists': playlists})

            
 
def lista_albumes_usuario_api(request, nombre_usuario):

    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[2]}'}
    response = requests.get(f"{settings.API_BASE_URL}{nombre_usuario}/albumes", headers=headers)
    albumes = response.json()
    return render(request, 'usuarios/lista_albumes_usuario.html', {
        'lista_albumes': albumes,
        'nombre_usuario': nombre_usuario
    })


def lista_usuarios_completa_api(request):

    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[2]}'}
    url = f"{settings.API_BASE_URL}usuarios/lista_usuarios_completa/"    
    response = requests.get(url, headers=headers)
  
    if response.status_code == 200:
        usuarios = response.json()
        return render(request, 'usuarios/lista_usuarios_completa.html', {
            'usuarios': usuarios
        })
    else:
        return render(request, 'usuarios/lista_usuarios_completa.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })
    

def lista_canciones_api(request):
   
    headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[2]}'}
    url = f"{settings.API_BASE_URL}canciones/lista_canciones_completa/"    
    response = requests.get(url, headers=headers)
        
    if response.status_code == 200:
        canciones = response.json()
        return render(request, 'canciones/lista_canciones_completa.html', {
            'canciones': canciones
        })
    else:
        return render(request, 'canciones/lista_canciones_completa.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })


def canciones_por_genero_api(request):
   
    headers = {'Authorization': f'Token {settings.AUTH_TOKEN}'}
        
    response = requests.get(f"{settings.API_BASE_URL}canciones/generos/", headers=headers)
        
    if response.status_code == 200:
        canciones = response.json()
        return render(request, 'canciones/canciones_genero.html', {
                'canciones': canciones
        })
    else:
        return render(request, 'canciones/canciones_genero.html', {
            'error': f"Error {response.status_code}: {response.text}"
        })
            
 

   
