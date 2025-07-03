import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import openai

# Configuración de la API de OpenAI
openai.api_key = "TU_API_KEY"  # Reemplaza con tu clave de API de OpenAI

# Lista de usuarios válidos
usuarios_validos = ["Paola", "Juan", "Maria", "Carlos"]

# Función para interactuar con IA
def interactuar_con_ia():
    def enviar_pregunta():
        pregunta = pregunta_entry.get()
        if pregunta.lower() == "salir":
            ia_window.destroy()
            return
        try:
            respuesta = openai.Completion.create(
                engine="text-davinci-003",
                prompt=pregunta,
                max_tokens=100,
                temperature=0.7
            )
            respuesta_label.config(text=f"JD: {respuesta.choices[0].text.strip()}")
        except Exception as e:
            respuesta_label.config(text=f"Error: {e}")

    ia_window = tk.Toplevel()
    ia_window.title("Módulo de IA")
    tk.Label(ia_window, text="Escribe tu pregunta:").pack(pady=5)
    pregunta_entry = tk.Entry(ia_window, width=50)
    pregunta_entry.pack(pady=5)
    tk.Button(ia_window, text="Enviar", command=enviar_pregunta).pack(pady=5)
    respuesta_label = tk.Label(ia_window, text="", wraplength=400, justify="left")
    respuesta_label.pack(pady=10)

# Función para registrar un nuevo usuario
def registrar_usuario():
    def guardar_usuario():
        nombre = nombre_entry.get().strip()
        correo = correo_entry.get().strip()
        if nombre and correo:
            with open("usuarios.txt", "a") as file:
                file.write(f"{nombre},{correo}\n")
            messagebox.showinfo("Registro exitoso", f"Gracias {nombre}, te has registrado con éxito.")
            registro_window.destroy()
        else:
            messagebox.showerror("Error", "El nombre y el correo no pueden estar vacíos.")

    registro_window = tk.Toplevel()
    registro_window.title("Registro de Usuario")
    tk.Label(registro_window, text="Ingresa tu nombre:").pack(pady=5)
    nombre_entry = tk.Entry(registro_window, width=30)
    nombre_entry.pack(pady=5)
    tk.Label(registro_window, text="Ingresa tu correo electrónico:").pack(pady=5)
    correo_entry = tk.Entry(registro_window, width=30)
    correo_entry.pack(pady=5)
    tk.Button(registro_window, text="Registrar", command=guardar_usuario).pack(pady=10)

# Función principal
def main():
    def validar_usuario():
        guess = usuario_entry.get().strip()
        if guess in usuarios_validos:
            messagebox.showinfo("Usuario Correcto", f"¡Hola {guess}! Tu usuario es CORRECTO.")
            mostrar_opciones_usuario_valido()
        else:
            messagebox.showwarning("Usuario Incorrecto", "Tu usuario es INCORRECTO.")
            mostrar_opciones_usuario_incorrecto()

    def mostrar_opciones_usuario_valido():
        opciones_window = tk.Toplevel()
        opciones_window.title("Opciones para Usuario Válido")
        tk.Label(opciones_window, text="¿Qué deseas hacer?").pack(pady=5)
        tk.Button(opciones_window, text="Iniciar módulo de aprendizaje con IA", command=interactuar_con_ia).pack(pady=5)
        tk.Button(opciones_window, text="Salir", command=opciones_window.destroy).pack(pady=5)

    def mostrar_opciones_usuario_incorrecto():
        opciones_window = tk.Toplevel()
        opciones_window.title("Opciones para Usuario Incorrecto")
        tk.Label(opciones_window, text="¿Qué deseas hacer?").pack(pady=5)
        tk.Button(opciones_window, text="Registrarme", command=registrar_usuario).pack(pady=5)
        tk.Button(opciones_window, text="Usar reconocimiento facial", command=lambda: messagebox.showinfo("Reconocimiento Facial", "Reconocimiento facial exitoso. Bienvenido de nuevo.")).pack(pady=5)
        tk.Button(opciones_window, text="Salir", command=opciones_window.destroy).pack(pady=5)

    # Ventana principal
    root = tk.Tk()
    root.title("JD - Acompañante Virtual")
    tk.Label(root, text="¡QUE TAL!, bienvenido. Soy Jd, tu Acompañante virtual. ¿En qué puedo ayudarte hoy?").pack(pady=10)
    tk.Label(root, text="Ingresa tu Usuario:").pack(pady=5)
    usuario_entry = tk.Entry(root, width=30)
    usuario_entry.pack(pady=5)
    tk.Button(root, text="Validar Usuario", command=validar_usuario).pack(pady=10)
    root.mainloop()

# Llamada al programa principal
if __name__ == "__main__":
    main()