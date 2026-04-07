import os
import json
import urllib.parse
from flask import Flask, render_template, abort

app = Flask(__name__,
           static_folder='static',  # carpeta static dentro de app
           static_url_path='/static')  # URL pública

# Función para cargar los datos del JSON de forma segura
def cargar_datos():
    # Buscamos el archivo novelas.json en la misma carpeta que este app.py
    ruta_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'novelas.json')
    
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route("/")
def index():
    data = cargar_datos()
    # Obtenemos las llaves y ordenamos
    lista_novelas = sorted(list(data.keys()))
    return render_template("index.html", novelas=lista_novelas)

# CAMBIO CLAVE: Usamos <path:nombre> para aceptar comas, espacios y puntos
@app.route("/novela/<path:nombre>")
def ver_novela(nombre):
    data = cargar_datos()
    
    # Decodificamos el nombre por si el navegador lo envió con códigos como %20 o %2C
    nombre_decodificado = urllib.parse.unquote(nombre)
    
    # Verificamos si la novela existe en nuestro JSON
    if nombre_decodificado not in data:
        # Si no lo encuentra directo, intentamos buscarlo tal cual viene (por si acaso)
        if nombre not in data:
            abort(404)
        else:
            nombre_decodificado = nombre
    
    volumenes = data[nombre_decodificado]
    return render_template("novela.html", nombre=nombre_decodificado, volumenes=volumenes)

if __name__ == "__main__":
    app.run(debug=True)