from flask import Flask, request
from flask_cors import  CORS
from Analizador import analizador


app = Flask(__name__)
app.config["DEBUG"]

CORS(app)
@app.route('/enviar', methods =['POST'])
def obtenerDatos():
    dato = request.data

    print("Solo Para Debug")
    return dato

app.run(debug = True)
