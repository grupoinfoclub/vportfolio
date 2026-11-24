# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.urls import path,include,re_path
from appportfolio import views
from appportfolio.views import *

# servicio de ficheros estáticos durante el desarrollo
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
# servicio de ficheros estáticos durante el servidor
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home,name='home'),
    #re_path('',views.home,name='home'),
    path('sobremi/',views.sobremi,name='sobremi'),
    re_path('experiencias/',views.experiencias,name='experiencias'),
    re_path('estudios/',views.estudios,name='estudios'),
    re_path('habilidades/',views.habilidades,name='habilidades'),
    re_path('diplomas',views.diplomas,name='diplomas'),
    re_path('certificados/',views.certificados,name='certificados'),  #para home.html
    re_path('enlaces/',views.enlaces,name='enlaces'), 
    #re_path('cerrar/',views.cerrar,name='cerrar'),
    #re_path('Login/', views.Login,name='Login'),
    #re_path('ver_experiencia/<int:id>/', views.ver_experiencia,name='ver_experiencia'),
    re_path(r'^(?P<id>\d+)/ver_experiencia$', views.ver_experiencia,name='ver_experiencia'),

    re_path(r'^cerrar/$', views.cerrar, name='cerrar'),
    path('accounts/', include('allauth.urls')),
    #re_path(r'^login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    #re_path(r'^logout/$', auth_views.LogoutView.as_view(), name="logout"),  # cerrar sistema
    #path('signup/', views.signup, name='signup'), # acceso al sistema
    path('Login/', views.Login, name='Login'),
    #path('Register/', views.Register, name='Register'),
    #path('Signup/', views.Signup, name='Signup'),
    re_path(r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),  #acceso al sistema
    path('eliminarExperiencia/<int:pk>/', views.eliminarExperiencia, name='eliminarExperiencia'),
    path('cargardatos/', views.cargardatos, name='cargardatos'),
    path("proyectos/", listar_proyectos, name="listar_proyectos"),
    path("carrusel/", carrusel, name="carrusel"),
    path("blog/", blog, name="blog"),
    path("crear_post/", crear_post, name="crear_post"),
    path('post/<int:id>/', views.ver_post, name='ver_post'),
    path('generar-qr/', views.generar_qr, name='generar_qr'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_pdf/', dashboard_pdf, name='dashboard_pdf'),
    path('listar_cursos/', views.listar_cursos, name='listar_cursos'),
    path('listar_bases/', views.listar_bases, name='listar_bases'),
    re_path(r'^main/$',views.sobremi,name='principal'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
