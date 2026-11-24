# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http  import HttpResponse
from appportfolio.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#paginacion
from django.contrib.auth import authenticate, get_user_model, login,logout  #todas son por defecto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect

#nuevas importaciones
from datetime import date, timedelta
import random
from django.db.models import Q

from appportfolio.forms import *
from django.shortcuts import render, get_object_or_404

#nueva importación
from django.core.paginator import Paginator

#QR
import qrcode
from io import BytesIO

from django.db.models import Count, Avg, Max
from django.contrib.auth.decorators import login_required

#PDF
import json
import base64
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

#Mongodb
from pymongo import MongoClient



################################################
# 1 - home
################################################

'''
def home(request):
    print("hola estoy en home") 
    nombre='Alfonso'
    # select * from Experiencias order by nombre_categoria desc;
    lista_experiencias = Experiencia.objects.all().order_by('-id')  
    for r in lista_experiencias:
        print(str(r.empresa))
        
    context = {'nombre':nombre, 'lista_experiencias':lista_experiencias}
    return render(request, 'home.html', context=context)
'''

'''
def home(request):
    print("hola estoy en home") 
    nombre = 'Alfonso'

    # Consulta: ordenado por ID
    lista_experiencias = Experiencia.objects.all().order_by('-id')

    # --- PAGINACIÓN ---
    paginator = Paginator(lista_experiencias, 2)  # 2 registros por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'nombre': nombre,
        'page_obj': page_obj,      # Enviamos el objeto paginado
        'lista_experiencias': page_obj.object_list  
    }

    return render(request, 'home.html', context)
'''


def home(request):
    print("hola estoy en home") 
    nombre = 'Alfonso'

    # --- BUSCADOR ---
    query = request.GET.get("q", "")
    lista = Experiencia.objects.all().order_by('-id')
    total_registros = lista.count()
    print(f"Total de registros: {total_registros}")

    if query:
        lista = lista.filter(empresa__icontains=query)

    # --- PAGINACIÓN ---
    paginator = Paginator(lista, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'nombre': nombre,
        'lista_experiencias': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'total_registros':total_registros,
    }

    return render(request, 'home.html', context)
  
################################################
# 2 - experiencias
################################################

def experiencias(request):
    lista_experiencias = Experiencia.objects.all()  # select * from Experiencias;
    page = request.GET.get('page')
    paginator = Paginator(lista_experiencias, 2)  # 2 registros por página
    if page == None:
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages
        request.session["pagina"] = page
    else:
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_experiencias = paginator.get_page(page)
    except PageNotAnInteger:
        lista_experiencias = paginator.page(1)
    except EmptyPage:
        lista_experiencias = paginator.page(paginator.num_pages)

    context = {'lista_experiencias': lista_experiencias}
    return render(request, 'experiencias.html', context=context)

################################################
# 3 -  estudios
################################################

def estudios(request):
    lista_estudios = ''
    context = {'lista_estudios': lista_estudios}
    return render(request, 'estudios.html', context=context)

################################################
# 4 -  habilidades
################################################

def habilidades(request):
    #lista_habilidades = Habilidad.objects.all()
    lista_habilidades =""
    context = {'lista_habilidades': lista_habilidades}
    return render(request, 'estudios.html', context=context)

################################################
# 5 -  sobremi
################################################

def sobremi(request):
    print("hola estoy en sobremi") 
    nombre='ALFONSO'
    edad=59
    telefono='674834567'
    cargo='PEON CAMINERO'
    #select * from Categoria
    listaCategorias=Categoria.objects.all().order_by('-nombre_categoria')
    for r in listaCategorias:
        print(str(r.nombre_categoria))
    context = {'nombre':nombre, 'edad':edad, 'telefono':telefono,
               'cargo':cargo,'listaCategorias':listaCategorias}
    return render(request, 'sobremi.html', context=context)

################################################
# 6 -  diplomas
################################################

def diplomas(request):
    lista_diplomas = ''
    context = {'lista_diplomas': lista_diplomas}
    return render(request, 'diplomas.html', context=context)

################################################
# 7 -  certificados
################################################

def certificados(request):
    lista_certificados = ''
    context = {'lista_certificados': lista_certificados}
    return render(request, 'certificados.html', context=context)

################################################
# 8 -  enlaces
################################################

def enlaces(request):
    lista_urls = ''
    context = {'lista_urls': lista_urls}
    return render(request, 'enlaces.html', context=context)

'''
def formacion(request):
    formaciones = Formacion.objects.all().order_by('id')
    for f in formaciones:
        print(str(f.id) + " " + str(f.estudio) + str(f.anyo))
    context = {'formaciones': formaciones}
    return render(request, 'formacion.html', context=context)
'''

def ver_experiencia(request,id):
    expe_id=id
    experiencia = Experiencia.objects.get(id=expe_id)
    context = {'experiencia': experiencia}
    return render(request, 'ver_experiencia.html',context=context)

# ####################### NUEVAS ######################################################

#CERRAR LA SESION DEL USUARIO
def cerrar(request):
    username = request.user.username
    password = request.user.password
    idusuario = request.user.id
    print("logout.................. " + username + "clave=" + str(password) + "id=" + str(idusuario))
    user = authenticate(request, username=username, password=password)
    # desconectamos al usuario
    logout(request)
    return redirect('/')

def Login(request):
    request.user.username = nombre
    request.user.password = clave
    context = {'nombre': nombre, 'clave': clave}
    return render(request, 'home.html', context=context)

def eliminarExperiencia(request, pk):
    print("ELIMINAR")
    expe_id=pk
    experiencia = Experiencia.objects.get(id=expe_id)
    #experiencia = get_object_or_404(Experiencia, pk=pk)
    if request.method == 'POST':
        experiencia.delete()
        return redirect('home')
    return render(request, 'eliminar_experiencia.html', {'experiencia': experiencia}) 
    
def cargar_proyectos():
    if Proyecto.objects.count() >= 20:
        return "Ya existen 20 o más registros. No se insertó nada."

    titulos = [
        "Sistema de Reservas",
        "Gestor de Inventario",
        "Aplicación de Tareas",
        "CRM para empresa",
        "Tienda Online",
        "Blog Personal",
        "Gestor de Notas",
        "API de Productos",
        "App de Finanzas",
        "Chat en tiempo real",
        "Sistema de Facturación",
        "Dashboard de Ventas",
        "Formulario Inteligente",
        "Aplicación de Viajes",
        "Sistema Escolar",
        "Plataforma de Cursos",
        "Control de Empleados",
        "Red Social Interna",
        "Monitor de Servidores",
        "Plataforma Streaming"
    ]

    for i in range(20):
        Proyecto.objects.create(
            titulo=titulos[i],
            descripcion="Proyecto de prueba generado automáticamente.",
            fecha=date.today() - timedelta(days=random.randint(1, 2000)),
            tecnologias=random.choice(["Python, Django", "Java, Spring", "JavaScript, React", "PHP, Laravel"]),
            precio=random.uniform(500, 5000)
        )

    return "20 proyectos creados con éxito"    

def cargardatos(request):
    resultado = cargar_proyectos()
    return HttpResponse(resultado)
    
def listar_proyectos(request):
    minimo=800
    maximo=2000
    tecnologia = "django"
    
    '''
    lista = Proyecto.objects.all()
    '''
    
    # FILTRO POR PRECIO
    '''
    lista = Proyecto.objects.filter(precio__gte=minimo, precio__lte=maximo)
    '''
    
    # FILTRO POR TECNOLOGÍA
    '''
    lista = Proyecto.objects.filter(tecnologias__icontains=tecnologia)
    '''
    
    # filtro and
    '''
    lista = Proyecto.objects.filter(precio__gte=minimo,precio__lte=maximo,tecnologias__icontains=tecnologia)
    '''
    
    #filtro OR
    '''
    lista = Proyecto.objects.filter(Q(precio__gte=minimo, precio__lte=maximo) | Q(tecnologias__icontains=tecnologia))
    '''
   
    #proyectos cuyo precio y año 2025 o que contengan “django” en tecnologías.
    lista = Proyecto.objects.filter(
    (Q(precio__gte=minimo, precio__lte=maximo) & Q(fecha__year=2025)) | Q(tecnologias__icontains=tecnologia))
    
    return render(request, "listar_proyectos.html", {
        "lista_proyectos": lista
    })
    
def carrusel(request):
    #experiencia = Experiencia.objects.get(id=expe_id)
    galeria="DIPLOMAS" 
    return render(request, 'carrusel.html', {'galeria': galeria})  

def blog(request):
    lista_posts = Post.objects.all().order_by('-fecha')    
    return render(request, 'blog.html', {'lista_posts': lista_posts})  

def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog')   # la página del listado
    else:
        form = PostForm()

    return render(request, "crear_post.html", {"form": form})
    

def ver_post(request, id):
    # Obtener el post por id o mostrar 404 si no existe
    post = get_object_or_404(Post, id=id)
    # Pasar el post al template
    return render(request, 'blog.html', {'post': post})    
    
def generar_qr(request):
    empresa = request.GET.get("empresa", "")

    if not empresa:
        return HttpResponse("No se recibió nombre de empresa.")

    # Crear QR
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(empresa)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir imagen a PNG
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename=qr_{empresa}.png'
    return response    
    

#@login_required
def dashboard(request):
    # KPIs
    total_experiencias = Experiencia.objects.count()
    total_proyectos = Proyecto.objects.count()
    total_posts = Post.objects.count()
    proyecto_mas_caro = Proyecto.objects.aggregate(Max('precio'))['precio__max']

    # Gráfico: proyectos por tecnología
    proyectos_tecnologia = (
        Proyecto.objects
        .values('tecnologias')
        .annotate(total=Count('id'))
    )

    # Gráfico: proyectos por año
    proyectos_anyo = (
        Proyecto.objects
        .values('fecha__year')
        .annotate(total=Count('id'))
        .order_by('fecha__year')
    )

    # Precio medio
    precio_medio = Proyecto.objects.aggregate(Avg('precio'))['precio__avg']

    context = {
        'total_experiencias': total_experiencias,
        'total_proyectos': total_proyectos,
        'total_posts': total_posts,
        'proyecto_mas_caro': proyecto_mas_caro,
        'precio_medio': round(precio_medio, 2) if precio_medio else 0,
        'proyectos_tecnologia': list(proyectos_tecnologia),
        'proyectos_anyo': list(proyectos_anyo),
    }

    return render(request, 'dashboard.html', context)
    

def dashboard_pdf(request):
    data = json.loads(request.body)

    # Decodificar imágenes
    def decode_img(img_base64):
        img_data = img_base64.split(',')[1]
        return ImageReader(BytesIO(base64.b64decode(img_data)))

    tecnologias_img = decode_img(data['tecnologias'])
    anyo_img = decode_img(data['anyo'])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="dashboard.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # 📝 TÍTULO
    p.setFont("Helvetica-Bold", 18)
    p.drawString(2*cm, height - 2*cm, "📊 Dashboard de Proyectos")

    # 🧮 KPIs
    p.setFont("Helvetica", 12)
    y = height - 4*cm

    p.drawString(2*cm, y, f"Total experiencias: {Experiencia.objects.count()}")
    p.drawString(2*cm, y-1*cm, f"Total proyectos: {Proyecto.objects.count()}")
    p.drawString(2*cm, y-2*cm, f"Total posts: {Post.objects.count()}")

    proyecto_caro = Proyecto.objects.aggregate(Max('precio'))['precio__max']
    p.drawString(2*cm, y-3*cm, f"Proyecto más caro: {proyecto_caro} €")

    # 📊 GRÁFICO 1
    p.drawImage(tecnologias_img, 2*cm, y-10*cm, width=16*cm, height=6*cm)

    p.showPage()

    # 📈 GRÁFICO 2
    p.setFont("Helvetica-Bold", 14)
    p.drawString(2*cm, height - 2*cm, "Proyectos por Año")

    p.drawImage(anyo_img, 2*cm, height - 14*cm, width=16*cm, height=6*cm)

    # 📝 TEXTO EXPLICATIVO
    p.setFont("Helvetica", 11)
    p.drawString(2*cm, height - 16*cm,
        "Este informe muestra la evolución de los proyectos y tecnologías utilizadas.")

    p.save()
    return response
    
def listar_cursos(request):
    # Conectar a MongoDB
    client = MongoClient('localhost', 27017)
    
    # Seleccionar base de datos y colección
    db = client['formaciondb']
    coleccion = db['listacursos']
    
    # Obtener todos los cursos
    cursos = list(coleccion.find())
    
    # Cerrar conexión
    client.close()
    
    # Pasar datos al template
    context = {
        'cursos': cursos,
        'total_cursos': len(cursos)
    }
    return render(request, 'lista_cursos.html', context=context)   

def listar_bases(request):
    """Versión simple: solo lista nombres"""
    try:
        client = MongoClient('localhost', 27017)
        bases = [db for db in client.list_database_names() 
                if db not in ['admin', 'local', 'config']]
        client.close()
        
        return render(request, 'bases_datos.html', {'bases_datos': bases,'total': len(bases)})
    except:
        return render(request, 'bases_datos.html', {'bases_datos': [],'total': 0,'error': True})

def principal(request):
    print("hola estoy en home")
    return HttpResponse('<h1>hola</h1>')