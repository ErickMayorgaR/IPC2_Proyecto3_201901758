from django.shortcuts import render
from .forms import infoForm, recibir_form, codigo_form
import requests
# Create your views here.

endpoint = 'http://127.0.0.1:5000/'

def main(request):
    contexto = {
    }
    if request.method == "POST":
        form = infoForm(request.POST, request.FILES)

        if form.is_valid():
            doc = request.FILES['file'].read()
            doc = doc.decode('utf-8')

            #files = {'file': doc}

            r = requests.post(endpoint + '/enviar', data = doc)
            r1 = r.status_code

            r3 = r.text
            r4 = r.request
            r5 = r.content
            contexto = {
                "datosEntrada1": doc,
                'datosSalida1': r3
            }

    return render(request, 'main.html', contexto)

def fecha_usuario(request):
    datos = ["a", "b", "c", "d"]
    conteo = [1, 2, 3, 4]
    contexto = {

    }

    if request.method == "POST":
        form = recibir_form(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['Fecha']

            #files = {'file': doc}
            r = requests.post(endpoint + '/fusuario', data = fecha);
            r3 = r.text
            r1 = r.json()
            labels = r1["Usuarios"]
            conteo = r1['Cantidad']

            contexto = {
                "labels": labels,
                'conteo': conteo
            }

    return render(request, 'FechaUsuario.html', contexto)

def fecha_codigo(request):
    print("llego? ")
    contexto = {
    }
    if request.method == "GET":
        form = codigo_form(request.GET)
        if form.is_valid():
            codigo = form.cleaned_data['Codigo']

            r = requests.get(endpoint + 'fcodigo/' + codigo)
            r3 = r.text
            r1 = r.json()
            labels = r1["Fecha"]
            conteo = r1['Cantidad']

            contexto = {
                "labels": labels,
                'conteo': conteo,
                'codigo': codigo
            }
    return render(request, 'FechaCodigo.html', contexto)

def consultar_datos(request):
    contexto = {
    }
    if request.method == "GET":
        r = requests.get(endpoint + 'consulta/')
        r3 = r.text
        contexto = {
            'datosSalida1': r3
            }

    print("llego")
    return render(request, "Consultar.html", contexto)


def informacion(request):
    contexto = {

    }
    return render(request, "Informacion.html", contexto)


def documentacion(request):
    contexto = {
    }
    return render(request,'Documentacion.html',contexto)


#ruta = request.FILES.get('file')
 #           ruta = str(ruta)
 #directorio = 'XML/'
            #directorio += ruta

            #with open(ruta,'w', encoding='utf-8') as f:
                #f.write(doc)
                #f.close()
