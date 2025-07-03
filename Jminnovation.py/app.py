from flask import Flask, request, jsonify, render_template
import openai
import requests
import cohere
from PIL import Image
from ultralytics import YOLO


# Configura tu clave API de OpenAI
openai.api_key = "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"
# Asegúrate de que la clave API sea válida y esté activa

# Crea el objeto Flask
app = Flask(__name__)

# Lista de usuarios válidos
usuarios_validos = ["Paola", "Juan", "Maria", "Carlos"]

# Función para cargar usuarios desde el archivo
def cargar_usuarios():
    try:
        with open("usuarios.txt", "r") as file:
            for linea in file:
                valores = linea.strip().split(",")
                if len(valores) >= 2:  # Asegúrate de que haya al menos dos valores
                    nombre, correo = valores[:2]  # Toma solo los dos primeros valores
                    if nombre not in usuarios_validos:
                        usuarios_validos.append(nombre)
    except FileNotFoundError:
        # Si el archivo no existe, no hacemos nada
        pass

# Cargar usuarios al iniciar la aplicación
cargar_usuarios()

# Ruta para la página principal
@app.route("/")
def home():
    return render_template("index.html")  # Renderiza el archivo HTML principal

# Ruta para validar usuarios
@app.route("/validar_usuario", methods=["POST"])
def validar_usuario():
    data = request.json
    usuario = data.get("usuario", "").strip()
    if usuario in usuarios_validos:
        return jsonify({"valido": True, "mensaje": f"Bienvenido, {usuario}."})
    else:
        return jsonify({"valido": False, "mensaje": "Usuario no válido. Por favor, regístrate."})

# Ruta para registrar un nuevo usuario
@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    data = request.json
    nombre = data.get("nombre", "").strip()
    correo = data.get("correo", "").strip()
    if nombre and correo:
        # Guarda el usuario en un archivo de texto
        with open("usuarios.txt", "a") as file:
            file.write(f"{nombre},{correo}\n")
        # Agrega el usuario a la lista de usuarios válidos
        usuarios_validos.append(nombre)
        return jsonify({"mensaje": f"Gracias {nombre}, te has registrado con éxito."})
    else:
        return jsonify({"error": "El nombre y el correo no pueden estar vacíos."}), 400

# Ruta para el módulo de aprendizaje

# Configura tu clave API

co = cohere.Client("zV737OzHkM0DuMbvANvxmMdFN6OgbOmmUKcXgbRI")  # Reemplaza con tu clave API de Cohere

UNSPLASH_ACCESS_KEY = "neKo3RNDT5Sn6dtI7JcnTE_cq24RH1q12aNxTXZoOK0"  # Reemplaza con tu clave API de Unsplash
@app.route("/modulo_aprendizaje", methods=["POST"])
def modulo_aprendizaje():
    data = request.json
    pregunta = data.get("pregunta", "").strip()
    if not pregunta:
        return jsonify({"error": "No se proporcionó una pregunta"}), 400

    try:
        # Lista de palabras irrelevantes (stopwords)
        stopwords = {"qué", "es", "un", "una", "de", "la", "el", "los", "las", "por", "para", "con", "Como","y", "o", "a", "en", "que","para"}

        # Limpia la pregunta y elimina palabras irrelevantes
        palabras = pregunta.lower().split()
        palabras_clave = [palabra for palabra in palabras if palabra not in stopwords]
        consulta = " ".join(palabras_clave)

        # Genera una respuesta usando la Chat API de Cohere
        respuesta = co.chat(
            message=pregunta,
            chat_history=[],
            model="command-xlarge-nightly",
            temperature=0.7
        )
        texto_respuesta = respuesta.text.strip()

        # Busca imágenes relacionadas usando Unsplash
        url = f"https://api.unsplash.com/search/photos?query={consulta}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)

        # Verifica si la respuesta de Unsplash es exitosa
        if response.status_code != 200:
            return jsonify({"error": "Error al buscar imágenes en Unsplash. Verifica tu clave API."}), 500

        imagenes = response.json().get("results", [])
        urls_imagenes = [img["urls"]["small"] for img in imagenes[:3]]  # Máximo 3 imágenes

        # Devuelve la respuesta de texto y las imágenes
        if not imagenes:
         return jsonify({"respuesta": texto_respuesta, "imagenes": [], "mensaje": "No se encontraron imágenes relacionadas."})
        return jsonify({"respuesta": texto_respuesta, "imagenes": urls_imagenes})
    except Exception as e:
        return jsonify({"error": f"Error al procesar la pregunta: {str(e)}"}), 500
    


# Carga el modelo YOLOv8 (más reciente y compatible)
yolo_model = YOLO('yolov8s.pt')

# Diccionario de traducción YOLO inglés -> español
TRADUCCIONES_YOLO = {
    "person": "persona",
    "sports ball": "pelota",
    "dog": "perro",
    "cat": "gato",
    "car": "carro",
    "bicycle": "bicicleta",
    "cell phone": "teléfono móvil",
    "book": "libro",
    "bottle": "botella",
    "cup": "taza",
    "motorcycle": "motocicleta",
    "kids": "niños",
    # Agrega más según tus necesidades
}

@app.route('/reconocer_imagen', methods=['POST'])
def reconocer_imagen():
    try:
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se envió ninguna imagen'}), 400

        imagen = request.files['imagen']
        img = Image.open(imagen.stream)

        # Realiza la predicción
        results = yolo_model(img)
        objetos = []
        for r in results:
            for c in r.boxes.cls:
                nombre = yolo_model.model.names[int(c)]
                nombre_es = TRADUCCIONES_YOLO.get(nombre, nombre)
                objetos.append(nombre_es)

        if not objetos:
            return jsonify({'error': 'No se detectaron objetos en la imagen.'}), 200

        # Genera una descripción explicativa
        if len(objetos) == 1:
            descripcion = f"{objetos[0]}."
        elif len(objetos) == 2:
            descripcion = f"En la imagen se pueden observar un(a) {objetos[0]} y un(a) {objetos[1]}."
        else:
            descripcion = f"La imagen contiene principalmente: {', '.join(objetos[:-1])} y {objetos[-1]}."

        return jsonify({'descripcion': descripcion, 'objetos': objetos}), 200

    except Exception as e:
        print("Error en reconocimiento local:", e)
        return jsonify({'error': f'Error al procesar la imagen: {str(e)}'}), 200

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) # Cambia el puerto si es necesario
