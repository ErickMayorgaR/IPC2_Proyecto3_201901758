from django.shortcuts import render
from .forms import infoForm
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

            files = {'file': doc}
            contexto = {
                "datosEntrada1": doc
            }
            r = requests.post(endpoint + '/enviar', data = doc)
            contexto = {
                "datosEntrada1": doc,
                'datosSalida1': r
            }

    return render(request, 'main.html', contexto)

#ruta = request.FILES.get('file')
 #           ruta = str(ruta)
 #directorio = 'XML/'
            #directorio += ruta

            #with open(ruta,'w', encoding='utf-8') as f:
                #f.write(doc)
                #f.close()
