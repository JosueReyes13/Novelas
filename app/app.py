import os
import json
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
        return {} # Retorna un diccionario vacío si el archivo no existe

@app.route("/")
def index():
    data = cargar_datos()
    # Obtenemos las llaves (nombres de novelas) y las ordenamos alfabéticamente
    lista_novelas = sorted(list(data.keys()))
    
    return render_template("index.html", novelas=lista_novelas)

@app.route("/novela/<nombre>")
def ver_novela(nombre):
    data = cargar_datos()
    
    # Verificamos si la novela existe en nuestro JSON
    if nombre not in data:
        abort(404)
    
    # Obtenemos la lista de volúmenes asociada a esa novela
    volumenes = data[nombre]
    
    # Ya no necesitamos ordenar aquí porque el JSON ya tiene el orden que tú le diste
    return render_template("novela.html", nombre=nombre, volumenes=volumenes)

if __name__ == "__main__":
    app.run(debug=True)