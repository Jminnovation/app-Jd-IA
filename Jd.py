# Proyecto: JD - Acompañante Virtual con IA
# Autor: Jm Innovation
# Descripción: Aplicación interactiva de aprendizaje con IA
# Fecha: [16/04/2025]
# Versión: 1.0

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Ruta para la página principal
@app.route("/")
def home():
    return render_template("index.html")  # Renderiza el frontend

from Frontend import main  # Importa la función principal del frontend

if __name__ == "__main__":
    main()  # Llama al frontend
import os

# Mensaje de bienvenida
def mostrar_bienvenida():
    saludo = "¡QUE TAL!, bienvenido. Soy Jd, tu Acompañante virtual. ¿En qué puedo ayudarte hoy?"
    print(saludo)

# Lista de usuarios válidos
usuarios_validos = ["Paola", "Juan", "Maria", "Carlos" ,"Jeison"]

# Función para obtener el usuario
def get_guess():
    while True:
        guess = input("Ingresa tu Usuario: ").strip()
        if guess:
            return guess
        print("El usuario no puede estar vacío. Inténtalo de nuevo.")

# Función para registrar un nuevo usuario
@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    data = request.json
    if nombre and correo:
        with open("usuarios.txt", "a") as file:
            file.write(f"{nombre},{correo}\n")
        return jsonify({"mensaje": f"Gracias {nombre}, te has registrado con éxito."})
    else:
        return jsonify({"error": "El nombre y el correo no pueden estar vacíos."}), 400
    
print("Por favor, completa el formulario de registro.")
nombre = input("Ingresa tu nombre: ").strip()
correo = input("DIGITA TU CODIGO de PERFIL: ").strip()
#  // 
if nombre and correo:
        with open("usuarios.txt", "a") as file:
            file.write(f"{nombre},{correo}\n")
        print(f"Gracias {nombre}, Has, iniciado Secion con éxito.")
else:
        print("El nombre y el correo no pueden estar vacíos. Inténtalo de nuevo.")

# Función para validar usuarios
def get_guess():
    while True:
        guess = input("Ingresa tu Usuario: ").strip()
        if guess:
            return guess
        print("El usuario no puede estar vacío. Inténtalo de nuevo.")

@app.route("/validar_usuario", methods=["POST"])
def validar_usuario():
    data = request.json
    usuario = data.get("usuario", "").strip()
    if usuario in usuarios_validos:
        return jsonify({"valido": True, "mensaje": f"Bienvenido, {usuario}."})
    else:
        return jsonify({"valido": False, "mensaje": "Usuario no válido. Por favor, regístrate."})
    
# Módulo de aprendizaje (IA básica)
def modulo_aprendizaje():
    print("¡Bienvenido al módulo de aprendizaje!")
    print("Puedes preguntarme sobre temas básicos de programación o conceptos generales.")
    while True:
        pregunta = input("Escribe tu pregunta (o escribe 'salir' para volver al menú principal): ").strip()
        if pregunta.lower() == "salir":
            break
        else:
            # Respuesta básica (puedes integrar IA aquí)
            print(f"Interesante pregunta: '{pregunta}'. Estoy aprendiendo, pero pronto podré responder mejor.")

@app.route("/modulo_aprendizaje", methods=["POST"])
def modulo_aprendizaje():
    data = request.json
    pregunta = data.get("pregunta", "").strip()
    if pregunta.lower() == "salir":
        return jsonify({"mensaje": "Saliendo del módulo de aprendizaje."})
    else:
        # Respuesta básica (puedes integrar IA aquí)
        respuesta = f"Interesante pregunta: '{pregunta}'. Estoy aprendiendo, pero pronto podré responder mejor."
        return jsonify({"respuesta": respuesta})
    
# Función principal
def main():
    while True:
        guess = get_guess()
        if guess in usuarios_validos:
            print(f"😊 TU usuario es CORRECTO")
            print(f"iniciemos, {guess}, ¿cómo estás?")
            print("¿Qué haremos hoy?")
            print("A. seleccionar un módulo")
            break
        else:
            print("Tu usuario es INCORRECTO.")
            print("¿Olvidaste tu usuario o no estás registrado?")
            print("1. Volver a intentarlo")
            print("2. Registrarme")
            print("3. Usar reconocimiento facial")
            opcion = input("Elige una opción (1, 2 o 3): ").strip()
            if opcion == "1":
                continue  # Vuelve a pedir el usuario
            elif opcion == "2":
                print("Por favor, completa el formulario de registro.")
                nombre = input("Ingresa tu nombre: ").strip()
                correo = input("DIGITA TU CODIGO de PERFIL: ").strip()
                if nombre and correo:
                    with open("usuarios.txt", "a") as file:
                        file.write(f"{nombre},{correo}\n")
                    print(f"Gracias {nombre}, te has registrado con éxito.")
                else:
                    print("El nombre y el correo no pueden estar vacíos. Inténtalo de nuevo.")
            elif opcion == "3":
                print("Iniciando reconocimiento facial... (Pon Tu cara frente a la cámara)")
                print("Reconocimiento facial exitoso. Bienvenido de nuevo.")
                print("¿Qué haremos hoy?")
                print("A. seleccionar un módulo")
                print("B. Salir")
                sub_opcion = input("Elige una opción (A o B): ").strip()
                if sub_opcion == "A":
                    continue  # Regresa al inicio del ciclo principal
                elif sub_opcion == "B":
                    print("Saliendo...")
                    break  # Sale del ciclo y termina el programa
                else:
                    print("Opción no válida. Por favor, elige una opción válida.")
            else:
                print("Opción no válida. Por favor, elige una opción correcta.")
           
# Función `say` para mostrar un emoticon
def say(saludo, emoticon="😎"):
    print(emoticon)
    return

# Llamada al programa principal
if __name__ == "__main__":
    mostrar_bienvenida()
    main()
    say("Hola")

    if __name__ == "__main__":
         app.run(host="0.0.0.0", port=5000, debug=True)
         app.run(host="0.0.0.0", port=5500, debug=True)

