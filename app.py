from flask import Flask, request, jsonify, render_template, session
import openai
import requests
import cohere
import os
from PIL import Image
from ultralytics import YOLO
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.utils import websafe_encode, websafe_decode

# 🔐 Carga claves desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
co = cohere.Client(os.getenv("COHERE_API_KEY"))
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# 🔐 Configuración Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_por_defecto_insegura")

# 🔒 FIDO2
rp = PublicKeyCredentialRpEntity(id="localhost", name="JD App")
server = Fido2Server(rp)

usuarios_validos = ["Paola", "Juan", "Maria", "Carlos"]
USERS = {}

def cargar_usuarios():
    try:
        with open("usuarios.txt", "r") as file:
            for linea in file:
                valores = linea.strip().split(",")
                if len(valores) >= 2:
                    nombre, correo = valores[:2]
                    if nombre not in usuarios_validos:
                        usuarios_validos.append(nombre)
    except FileNotFoundError:
        pass

cargar_usuarios()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/validar_usuario", methods=["POST"])
def validar_usuario():
    data = request.json
    usuario = data.get("usuario", "").strip()
    if usuario in usuarios_validos:
        return jsonify({"valido": True, "mensaje": f"Bienvenido, {usuario}."})
    else:
        return jsonify({"valido": False, "mensaje": "Usuario no válido. Por favor, regístrate."})

@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    data = request.json
    nombre = data.get("nombre", "").strip()
    correo = data.get("correo", "").strip()
    if nombre and correo:
        with open("usuarios.txt", "a") as file:
            file.write(f"{nombre},{correo}\n")
        usuarios_validos.append(nombre)
        return jsonify({"mensaje": f"Gracias {nombre}, te has registrado con éxito."})
    else:
        return jsonify({"error": "El nombre y el correo no pueden estar vacíos."}), 400

@app.route("/modulo_aprendizaje", methods=["POST"])
def modulo_aprendizaje():
    data = request.json
    pregunta = data.get("pregunta", "").strip()
    if not pregunta:
        return jsonify({"error": "No se proporcionó una pregunta"}), 400

    try:
        stopwords = {"qué", "es", "un", "una", "de", "la", "el", "los", "las", "por", "para", "con", "como", "y", "o", "a", "en", "que"}
        palabras = pregunta.lower().split()
        palabras_clave = [palabra for palabra in palabras if palabra not in stopwords]
        consulta = " ".join(palabras_clave)

        respuesta = co.chat(
            message=pregunta,
            chat_history=[],
            model="command-xlarge-nightly",
            temperature=0.7
        )
        texto_respuesta = respuesta.text.strip()

        url = f"https://api.unsplash.com/search/photos?query={consulta}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": "Error al buscar imágenes en Unsplash. Verifica tu clave API."}), 500

        imagenes = response.json().get("results", [])
        urls_imagenes = [img["urls"]["small"] for img in imagenes[:3]]

        if not imagenes:
            return jsonify({"respuesta": texto_respuesta, "imagenes": [], "mensaje": "No se encontraron imágenes relacionadas."})
        return jsonify({"respuesta": texto_respuesta, "imagenes": urls_imagenes})
    except Exception as e:
        return jsonify({"error": f"Error al procesar la pregunta: {str(e)}"}), 500

# 🧠 Modelo YOLO
yolo_model = YOLO('yolov8s.pt')
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
    "scissors": "tijeras",
    "cohete": "cohete",
}

@app.route('/reconocer_imagen', methods=['POST'])
def reconocer_imagen():
    try:
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se envió ninguna imagen'}), 400

        imagen = request.files['imagen']
        img = Image.open(imagen.stream)
        results = yolo_model(img)
        objetos = []
        for r in results:
            for c in r.boxes.cls:
                nombre = yolo_model.model.names[int(c)]
                nombre_es = TRADUCCIONES_YOLO.get(nombre, nombre)
                objetos.append(nombre_es)

        if not objetos:
            return jsonify({'error': 'No se detectaron objetos en la imagen.'}), 200

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

@app.route("/webauthn/register/begin", methods=["POST"])
def webauthn_register_begin():
    usuario = request.json["usuario"]
    registration_data, state = server.register_begin(
        {"id": usuario.encode(), "name": usuario, "displayName": usuario},
        user_verification="required"
    )
    session["state"] = state
    return jsonify(registration_data)

@app.route("/webauthn/register/complete", methods=["POST"])
def webauthn_register_complete():
    usuario = request.json["usuario"]
    data = request.json["data"]
    state = session.get("state")
    auth_data = server.register_complete(state, data)
    USERS[usuario] = {"credential_data": auth_data.credential_data}
    return jsonify({"ok": True})

@app.route("/webauthn/authenticate/begin", methods=["POST"])
def webauthn_authenticate_begin():
    usuario = request.json["usuario"]
    creds = [USERS[usuario]["credential_data"]]
    auth_data, state = server.authenticate_begin(creds)
    session["state"] = state
    return jsonify(auth_data)

@app.route("/webauthn/authenticate/complete", methods=["POST"])
def webauthn_authenticate_complete():
    usuario = request.json["usuario"]
    data = request.json["data"]
    state = session.get("state")
    creds = [USERS[usuario]["credential_data"]]
    server.authenticate_complete(state, creds, data.credential_id, data.client_data, data.authenticator_data, data.signature)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

