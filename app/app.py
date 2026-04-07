import os
from flask import Flask, render_template, abort

app = Flask(__name__)

# Función auxiliar para obtener la ruta base de las novelas
def get_novelas_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Ajusta 'static/novelas' según tu estructura real
    return os.path.join(base_dir, 'static', 'novelas')

@app.route("/")
def index():
    path = get_novelas_path()
    lista_novelas = []
    if os.path.exists(path):
        lista_novelas = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return render_template("index.html", novelas=lista_novelas)

@app.route("/novela/<nombre>")
def ver_novela(nombre):
    path = get_novelas_path()
    novela_dir = os.path.join(path, nombre)
    
    # Verificamos si la carpeta de esa novela existe
    if not os.path.exists(novela_dir):
        abort(404) # Si no existe, enviamos error 404
    
    # Listamos todos los archivos .pdf dentro de esa carpeta
    volumenes = [f for f in os.listdir(novela_dir) if f.lower().endswith('.pdf')]
    # Los ordenamos alfabéticamente para que salgan en orden (Vol 1, Vol 2...)
    volumenes.sort()
    
    return render_template("novela.html", nombre=nombre, volumenes=volumenes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)