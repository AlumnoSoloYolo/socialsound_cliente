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
                return render(request, 'usuarios/crear-usuarios.html', {"formulario": formulario})
                
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



def usuario_editar(request, id):
   print("============ INICIO USUARIO_EDITAR ============")
   print(f"Método: {request.method}")
   print(f"ID: {id}")

   if request.method == "POST":
       try:
           print("1. Recibiendo POST en cliente")
           formulario = UsuarioUpdateForm(request.POST, request.FILES)
           
           print("2. Validando formulario...")
           if not formulario.is_valid():
               print("2.1 Formulario no válido:", formulario.errors)
               return render(request, 'usuarios/editar-usuario.html', {"formulario": formulario, "id": id})
               
           print("3. Formulario válido, preparando datos...")
           headers = crear_cabecera_contentType()
           datos = formulario.cleaned_data.copy()

           
           if not datos.get('password'):
             datos.pop('password', None)
       
           
             # Manejamos la foto de perfil
           if 'foto_perfil' in request.FILES:
                foto = request.FILES['foto_perfil']
                with foto.open('rb') as f:
                    foto_contenido = f.read()
                encoded = base64.b64encode(foto_contenido).decode('utf-8')
                datos['foto_perfil'] = f"data:{foto.content_type};base64,{encoded}"
           else:
                # Si no hay nueva foto, eliminamos el campo para mantener la existente
                datos.pop('foto_perfil', None)
            
           print("4. Datos limpios:", datos)
           
           url = f'http://127.0.0.1:8000/api/v1/usuarios/{id}/actualizar'
           print("6. Preparando petición PUT...")
           print("6.1 URL:", url)
           print("6.2 Headers:", headers)
           
           print("7. Enviando petición PUT...")
           response = requests.put(
               url,
               headers=headers,
               data=json.dumps(datos)
           )
           print("8. Respuesta recibida:")
           print(f"8.1 Status code: {response.status_code}")
           print(f"8.2 Contenido: {response.text}")
           
           if(response.status_code == requests.codes.ok):
               print("9. Petición exitosa, redirigiendo...")
               return redirect("lista_usuarios_completa")
           else:
               print("9. Error en la petición")
               print(f"9.1 Status code: {response.status_code}")
               print(f"9.2 Respuesta: {response.text}")
               response.raise_for_status()

       except HTTPError as http_err:
           print("ERROR - HTTPError:")
           print(f"Detalle: {http_err}")
           if(response.status_code == 400):
               errores = response.json()
               print(f"Errores de validación: {errores}")
               for error in errores:
                   formulario.add_error(error, errores[error])
               return render(request, 'usuarios/editar-usuario.html', {"formulario": formulario, "id": id})
           else:
               return mi_error_500(request)

       except Exception as err:
           print("ERROR - Exception general:")
           print(f"Tipo: {type(err)}")
           print(f"Detalle: {str(err)}")
           return mi_error_500(request)

   else:
       print("10. Método GET - Obteniendo datos del usuario...")
       try:
           usuario = helper.obtener_usuario(id)
           print("10.1 Usuario obtenido:", usuario)
           
           print("11. Inicializando formulario...")
           formulario = UsuarioForm(initial={
               'nombre_usuario': usuario['nombre_usuario'],
               'email': usuario['email'],
               'bio': usuario.get('bio', ''),
               'foto_perfil': usuario.get('foto_perfil', '')
           })
           print("11.1 Formulario inicializado")

       except Exception as err:
           print("ERROR - Al obtener usuario:")
           print(f"Tipo: {type(err)}")
           print(f"Detalle: {str(err)}")
           return mi_error_500(request)

   print("12. Renderizando template...")
   return render(request, 'usuarios/editar-usuario.html', {"formulario": formulario, "id": id})



def usuario_editar_nombre(request, usuario_id):
    usuario = helper.obtener_usuario(usuario_id)
    formulario = UsuarioActualizarNombreForm(request.POST or None, initial={'nombre_usuario': usuario['nombre_usuario']})
    
    if request.method == "POST":
        try:
            headers = crear_cabecera_contentType()
            datos = request.POST.copy()
            response = requests.patch(
                f'http://127.0.0.1:8000/api/v1/usuarios/actualizar/nombre/{usuario_id}',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                return redirect("lista_usuarios_completa")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    
    return render(request, 'usuarios/actualizar_nombre.html', {"formulario": formulario, "usuario": usuario})


def usuario_eliminar(request, usuario_id):
    if request.method == "POST":
        try:
            headers = crear_cabecera()
            response = requests.delete(
                f'http://127.0.0.1:8000/api/v1/usuarios/eliminar/{usuario_id}',
                headers=headers,
            )
            if response.status_code == requests.codes.ok:
                return redirect("lista_usuarios_completa")
            else:
                print(response.status_code)
                response.raise_for_status()
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        usuario = helper.obtener_usuario(usuario_id)
        return render(request, 'usuarios/eliminar_confirmacion.html', {'usuario': usuario})
    


def album_eliminar(request, id):
    if request.method == "POST":
        try:
            headers = crear_cabecera()
            response = requests.delete(
                f'http://127.0.0.1:8000/api/v1/albumes/{id}/eliminar/',
                headers=headers,
            )
            if response.status_code == requests.codes.ok:
                return redirect("lista_albumes")
            else:
                print(response.status_code)
                response.raise_for_status()
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        album = helper.obtener_album(id)
        return render(request, 'albums/eliminar_album.html', {'album': album})




def album_crear(request):
    print("Iniciando album_crear")
    print(f"Método: {request.method}")
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        print("Datos del formulario recibidos:", request.POST)
        
        if form.is_valid():
            print("Formulario válido")
            datos = form.cleaned_data.copy()
            print("Datos limpios iniciales:", datos)

            print("Datos POST:", request.POST)
            print("Datos FILES:", request.FILES)
            print("Datos limpiados del formulario:", datos)
            
       
            if 'usuario' in datos:
                usuario_id = datos['usuario']
                datos['usuario'] = int(usuario_id)
                print(f"ID de usuario a enviar: {datos['usuario']}")

            headers = crear_cabecera_contentType()

            if 'portada' in request.FILES:
                print("Procesando portada...")
                portada = request.FILES['portada']
                with portada.open('rb') as f:
                    portada_contenido = f.read()
                encoded = base64.b64encode(portada_contenido).decode('utf-8')
                datos['portada'] = f"data:{portada.content_type};base64,{encoded}"
                print("Portada procesada")
            else:
                datos.pop('portada', None)
                print("No se recibió portada")

            print("Datos finales a enviar:", datos)

            try:
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/albumes/crear/', 
                    headers=headers, 
                    json=datos  # Asegúrate de que los datos son serializables
                )
                print(f"Status code: {response.status_code}")
                print(f"Respuesta del servidor: {response.text}")

                if response.status_code in [200, 201]:
                    print("Álbum creado exitosamente")
                    return redirect('lista_albumes')
                else:
                    print(f"Error en la creación: {response.text}")
                    try:
                        errores = response.json()
                        for campo, mensaje in errores.items():
                            form.add_error(campo, mensaje)
                    except:
                        form.add_error(None, "Error al procesar la respuesta del servidor")
                    return render(request, 'albums/album_crear.html', {'formulario': form})
                    
            except requests.exceptions.RequestException as e:
                print(f"Error en la petición: {str(e)}")
                form.add_error(None, f"Error de conexión: {str(e)}")
                return render(request, 'albums/album_crear.html', {'formulario': form})
        else:
            print("Formulario inválido")
            print("Errores del formulario:", form.errors)
            
    else:
        print("GET recibido, mostrando formulario vacío")
        form = AlbumForm()
        
    return render(request, 'albums/album_crear.html', {'formulario': form})


def album_editar(request, id):
    print("Iniciando album_editar")
    print(f"Método: {request.method}")
    
    if request.method == 'POST':
        print("POST recibido")
        form = AlbumUpdateForm(request.POST, request.FILES)
        print("Datos del formulario:", request.POST)
        
        if form.is_valid():
            print("Formulario válido")
            datos = form.cleaned_data.copy()
            print("Datos limpios:", datos)

             # Obtener el álbum para verificar qué usuario está asociado
            album = helper.obtener_album(id)
            if album:
                # Asignar el usuario que ya está asociado al álbum
                datos['usuario'] = album['usuario']
            
            headers = crear_cabecera_contentType()

            if 'portada' in request.FILES:
                print("Procesando portada...")
                portada = request.FILES['portada']
                with portada.open('rb') as f:
                    portada_contenido = f.read()
                encoded = base64.b64encode(portada_contenido).decode('utf-8')
                datos['portada'] = f"data:{portada.content_type};base64,{encoded}"
                print("Portada procesada")
            else:
                datos.pop('portada', None)
                print("No se modificó la portada")

            print("Datos finales a enviar:", datos)
            try:
                response = requests.put(
                    f'http://127.0.0.1:8000/api/v1/albumes/{id}/editar/', 
                    headers=headers, 
                    json=datos
                )
                print(f"Status code: {response.status_code}")
                print(f"Respuesta: {response.text}")

                if response.status_code in [200, 201]:
                    print("Álbum actualizado exitosamente")
                    return redirect('lista_albumes')
                else:
                    print("Error en la actualización")
                    errores = response.json()
                    for campo, mensaje in errores.items():
                        form.add_error(campo, mensaje)
                    return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})
                    
            except requests.exceptions.RequestException as e:
                print(f"Error en la petición: {str(e)}")
                form.add_error(None, f"Error de conexión: {str(e)}")
                return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})
        else:
            print("Formulario inválido")
            print("Errores:", form.errors)
    else:
        print("GET recibido, obteniendo datos del álbum")
        try:
            # Obtener los datos actuales del álbum
            album = helper.obtener_album(id)
            print("Datos del álbum obtenidos:", album)
            
            # Inicializar el formulario con los datos existentes
            form = AlbumUpdateForm(initial={
                'titulo': album.get('titulo', ''),
                'artista': album.get('artista', ''),
                'descripcion': album.get('descripcion', '')
            })
        except Exception as e:
            print(f"Error al obtener álbum: {str(e)}")
            return redirect('lista_albumes')
            
    return render(request, 'albums/album_editar.html', {'formulario': form, 'id': id})




def album_editar_titulo(request, id):
    album = helper.obtener_album(id)
    formulario = AlbumActualizarTituloForm(request.POST or None, initial={'titulo': album['titulo']})
    
    if request.method == "POST":
        try:
            headers = crear_cabecera_contentType()
            datos = request.POST.copy()
            response = requests.patch(
                f'http://127.0.0.1:8000/api/v1/albumes/actualizar/titulo/{id}/',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                return redirect("lista_albumes")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    
    return render(request, 'albums/actualizar_titulo.html', {"formulario": formulario, "id": id})



def playlist_crear(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data.copy()
            datos['canciones'] = request.POST.getlist('canciones')

            try:
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/playlists/crear/',
                    headers=crear_cabecera_contentType(),
                    data=json.dumps(datos)
                )
                if response.status_code == requests.codes.ok:
                    return redirect('lista_playlists')
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = response.json()
                    for error in errores:
                        form.add_error(error, errores[error])
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return mi_error_500(request)
    else:
        form = PlaylistForm()
    return render(request, 'playlists/crear_playlist.html', {'formulario': form})


def playlist_editar(request, id):
    print("Iniciando playlist_editar")
    print(f"Método: {request.method}")

    try:
        # Obtener los datos actuales de la playlist
        playlist = helper.obtener_playlist(id)

        if not playlist or 'error' in playlist:
            print("Error: No se encontró la playlist")
            return redirect('lista_playlists')

        print("Datos de la playlist obtenidos:", playlist)
        
        usuario_id = playlist.get('usuario')  # Asignamos el usuario directamente de la playlist
    except Exception as e:
        print(f"Error al obtener playlist: {str(e)}")
        return redirect('lista_playlists')

    if request.method == 'POST':
        print("POST recibido")
        form = PlaylistUpdateForm(request.POST)

        print("Datos del formulario:", request.POST)

        if form.is_valid():
            print("Formulario válido")
            datos = form.cleaned_data.copy()
            print("Datos limpios:", datos)

            # Asignar usuario antes de enviar la petición
            datos['usuario'] = usuario_id
            headers = crear_cabecera_contentType()

            print("Datos finales a enviar:", datos)
            try:
                response = requests.put(
                    f'http://127.0.0.1:8000/api/v1/playlists/{id}/editar/', 
                    headers=headers, 
                    json=datos
                )
                print(f"Status code: {response.status_code}")
                print(f"Respuesta: {response.text}")

                if response.status_code in [200, 201]:
                    print("Playlist actualizada exitosamente")
                    return redirect('lista_playlists')
                else:
                    print("Error en la actualización")
                    errores = response.json()
                    for campo, mensaje in errores.items():
                        form.add_error(campo, mensaje)
                    
            except requests.exceptions.RequestException as e:
                print(f"Error en la petición: {str(e)}")
                form.add_error(None, f"Error de conexión: {str(e)}")

        else:
            print("Formulario inválido")
            print("Errores:", form.errors)

    else:
        print("GET recibido, precargando datos en el formulario")
        
        # Obtener solo los IDs de las canciones para preseleccionarlas en el select
        canciones_ids = [cancion['id'] for cancion in playlist.get('canciones', [])]
        print("IDs de canciones seleccionadas:", canciones_ids)
        
        # Inicializar el formulario con los datos existentes
        form = PlaylistUpdateForm(initial={
            'nombre': playlist.get('nombre', ''),
            'descripcion': playlist.get('descripcion', ''),
            'canciones': canciones_ids,  # Aquí asignamos solo los IDs de las canciones
            'publica': playlist.get('publica', False)
        })

    return render(request, 'playlists/editar_playlist.html', {'formulario': form, 'id': id})







    

















def detalle_album_crear(request):
    if request.method == 'POST':
        print("Solicitud POST recibida")
        form = DetalleAlbumForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            data = form.cleaned_data
          

            # Extrae el ID del álbum
            album_id = data.pop('album')
            print(f"ID del álbum extraído: {album_id}")

            headers = crear_cabecera_contentType()
            print("Encabezados de la solicitud:")
         
            response = requests.post(
                f'http://127.0.0.1:8000/api/v1/albumes/{album_id}/detalles/',
                json=data,  # Envía los datos como JSON
                headers=headers
            )

            print(f"Respuesta del backend: Código {response.status_code}")
            print("Contenido de la respuesta:")
            print(response.content)

            if response.status_code == 200:
                print("Detalle del álbum creado correctamente. Redirigiendo...")
                return redirect('lista_albumes')
            else:
                print("Error al crear el detalle del álbum. Redirigiendo...")
                return redirect('lista_albumes')
        else:
            print("Formulario no válido. Errores:")
            print(form.errors)
    else:
        print("Solicitud GET recibida. Mostrando formulario...")
        form = DetalleAlbumForm()

    return render(request, 'detalles_album/detalle_album_crear.html', {'formulario': form})



def detalle_album_editar(request, id):
    if request.method == "POST":
        try:
            formulario = DetalleAlbumForm(request.POST)
            if not formulario.is_valid():
                return render(request, 'detalles_album/detalle_album_actualizar.html', 
                            {"formulario": formulario, "id": id})
                
            headers = crear_cabecera_contentType()
            data = formulario.cleaned_data.copy()
            
            response = requests.put(
                f'http://127.0.0.1:8000/api/v1/albumes/detalles/{id}/editar/',
                headers=headers,
                json=data
            )
            
            if(response.status_code == requests.codes.ok):
                return redirect("lista_albumes")
            else:
                response.raise_for_status()
        except HTTPError as http_err:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'detalles_album/detalle_album_actualizar.html', 
                            {"formulario": formulario, "id": id})
            else:
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
            print("Formulario inicializado con:", formulario.initial)  
            
            return render(request, 'detalles_album/detalle_album_actualizar.html', 
                        {"formulario": formulario, "id": id})
                        
        except Exception as e:
            print(f"Error al obtener detalle: {str(e)}")
            # Aquí puedes manejar el error como prefieras
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








 

   
