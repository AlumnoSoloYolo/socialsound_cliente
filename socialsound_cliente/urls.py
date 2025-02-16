from django.urls import path
from .views import *



urlpatterns = [
     path('', index, name="index"),
     path('playlists/', lista_playlists_api, name='lista_playlists'),
     # path('usuarios/<str:nombre_usuario>/albumes/', lista_albumes_usuario_api, name='lista_albumes_usuario'),
     path('usuarios/lista_usuarios_completa/', lista_usuarios_completa_api, name="lista_usuarios_completa"),
     path('canciones/', lista_canciones_api, name='lista_canciones'),
     path('canciones/generos/', canciones_por_genero_api, name='canciones_por_genero_api'),
     path('usuarios/busqueda_usuarios', busqueda_usuarios_api, name='busqueda_usuarios'),
     path('usuarios/busqueda_avanzada/', usuario_busqueda_avanzada_api, name='usuarios_busqueda_avanzada'),
     path('albumes/busqueda_avanzada/', album_busqueda_avanzada_api, name='albumes_busqueda_avanzada'),
     path('canciones/busqueda_avanzada/', cancion_busqueda_avanzada_api, name='canciones_busqueda_avanzada'),
     path('playlists/busqueda_avanzada/', playlist_busqueda_avanzada_api, name='playlists_busqueda_avanzada'),
     path('usuario/crear/', usuario_crear, name='usuario_crear'),

]
