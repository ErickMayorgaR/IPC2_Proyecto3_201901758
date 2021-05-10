from flask import Flask, request
from flask_cors import  CORS
from Analizador import analizador

analizarEnvio = analizador()
app = Flask(__name__)
app.config["DEBUG"]

CORS(app)
@app.route('/enviar', methods =['POST'])
def obtenerDatos():
    dato = request.data
    dato = dato.decode('latin1')
    respuesta = analizarEnvio.analizar(dato)

    return respuesta


@app.route('/fusuario', methods = ["POST"])
def obtener_usuario_cantidad():
    fecha = request.data
    fecha = fecha.decode('utf-8')
    dict = analizarEnvio.devolver_fecha_usuarios(fecha)
    return dict

@app.route('/fcodigo/<codigo>')
def obtener_codigo_fecha(codigo = None):
    cod = codigo
    dict  = analizarEnvio.devolver_codigo_fecha(cod)
    return dict


@app.route('/consulta/')
def consultar():
    datos = analizarEnvio.consultar_datos()
    return datos

app.run(debug = True)
