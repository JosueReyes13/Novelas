import os
from flask import Flask, render_template, abort

# Al estar app.py dentro de la carpeta /app, Flask detecta automáticamente
# las carpetas templates/ y static/ si están en el mismo nivel.
app = Flask(__name__)

# Función para obtener la ruta de las novelas de forma dinámica
def get_novelas_path():
    # os.path.dirname(__file__) nos da la ruta de la carpeta 'app'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'static', 'novelas')

@app.route("/")
def index():
    path = get_novelas_path()
    lista_novelas = []
    
    # Verificamos si existe la carpeta para evitar errores en el despliegue
    if os.path.exists(path):
        lista_novelas = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        lista_novelas.sort() # Siempre es bueno ordenar la lista principal
        
    return render_template("index.html", novelas=lista_novelas)

@app.route("/novela/<nombre>")
def ver_novela(nombre):
    path = get_novelas_path()
    novela_dir = os.path.join(path, nombre)
    
    if not os.path.exists(novela_dir):
        abort(404)
    
    # Filtramos solo archivos PDF
    volumenes = [f for f in os.listdir(novela_dir) if f.lower().endswith('.pdf')]
    volumenes.sort()
    
    return render_template("novela.html", nombre=nombre, volumenes=volumenes)

# Esto es para que puedas seguir probando localmente con python app/app.py
if __name__ == "__main__":
    app.run(debug=True)