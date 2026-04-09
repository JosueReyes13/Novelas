import os
import json
import urllib.parse
from flask import Flask, render_template, abort, jsonify

app = Flask(__name__,
           static_folder='static',
           static_url_path='/static')

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
    # Obtenemos las llaves (títulos de las novelas) y ordenamos
    lista_novelas = sorted(list(data.keys()))
    return render_template("index.html", novelas=lista_novelas)

# Usamos <path:nombre> para aceptar comas, espacios y puntos
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
    
    # Obtenemos los datos de la novela (sinopsis y volumenes)
    novela_data = data[nombre_decodificado]
    sinopsis = novela_data.get('sinopsis', 'Sinopsis no disponible próximamente...')
    volumenes = novela_data.get('volumenes', [])
    
    # Pasamos todos los datos al template
    return render_template("novela.html", 
                         nombre=nombre_decodificado, 
                         volumenes=volumenes,
                         sinopsis=sinopsis)

# NUEVO ENDPOINT PARA EL BUSCADOR
@app.route('/api/novelas')
def api_novelas():
    """Endpoint para obtener la lista de títulos de novelas (para el buscador)"""
    data = cargar_datos()
    lista_novelas = sorted(list(data.keys()))
    return jsonify(lista_novelas)  # Usamos jsonify en lugar de json.dumps

if __name__ == "__main__":
    app.run(debug=True)