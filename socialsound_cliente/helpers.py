import requests
from django.conf import settings


# def crear_cabecera():
#     return {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}

class helper:
    
    def obtener_token_session(usuario,password):
        token_url = f'{settings.API_URL}oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'musicapp',
            'client_secret': 'musicapp',
        }
        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))
        

    def obtener_usuario(usuario_id):
        headers = {'Authorization': f'Token {settings.AUTH_TOKEN}'} 
        response = requests.get(f'{settings.API_URL}usuarios/{str(usuario_id)}', headers=headers)
        usuario = response.json()
        return usuario
    

    def obtener_albumes_select():
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        response = requests.get(f'{settings.API_URL}albumes/', headers=headers)
        albumes = response.json()
        
        lista_albumes = [("", "Seleccione un álbum")]
        for album in albumes:
            lista_albumes.append((album["id"], album["titulo"]))
        return lista_albumes
    

    def obtener_usuarios_select():
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        response = requests.get(f'{settings.API_URL}usuarios/', headers=headers)
        usuarios = response.json()
        
        lista_usuarios = [("", "Seleccione un usuario")]
        for usuario in usuarios:
            lista_usuarios.append((usuario["id"], usuario["nombre_usuario"]))
        return lista_usuarios
    
    def obtener_album(id):
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        response = requests.get(f'{settings.API_URL}albumes/{id}/', headers=headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Error al obtener álbum: {response.text}")
    
 

    def obtener_detalle_album(id):
        print("Iniciando obtener_detalle_album")
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        
     
        response = requests.get(f'{settings.API_URL}albumes/detalles/{id}', headers=headers)
      
        return response.json()
    
    def obtener_canciones_select():
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'} 
        response = requests.get(f'{settings.API_URL}canciones', headers=headers)
        canciones = response.json()
        
        lista_canciones = []
        for cancion in canciones:
            lista_canciones.append((cancion["id"], f"{cancion['titulo']} - {cancion['artista']}"))
        return lista_canciones

    def obtener_playlist(id):
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'} 
        response = requests.get(f'{settings.API_URL}playlists/{id}', headers=headers)
        return response.json()

    def obtener_playlists_select():
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        response = requests.get(f'{settings.API_URL}playlists/', headers=headers)
        playlists = response.json()
        
        lista_playlists = [("", "Seleccione una playlist")]
        for playlist in playlists:
            lista_playlists.append((playlist["id"], playlist["nombre"]))
        return lista_playlists


    def obtener_canciones_playlist(playlist_id):
        headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
        response = requests.get(f'{settings.API_URL}playlists/{playlist_id}/', headers=headers)
        playlist = response.json()
        return [cancion.get(id) for cancion in playlist.get('canciones', [])]
    

    # def obtener_like(id):
    #     headers = {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}
    #     response = requests.get(f'{settings.API_URL}likes/{id}/', headers=headers)
    #     return response.json()
        
  