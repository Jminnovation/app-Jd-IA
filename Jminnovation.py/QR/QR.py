
import qrcode

# Contenido del código QR
contenido = "https://7bbe-179-19-62-81.ngrok-free.app/"

# Crear el código QR
qr = qrcode.QRCode(
    version=1,  # Controla el tamaño del QR (1 es el más pequeño)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
    box_size=8,  # Tamaño de cada cuadro del QR
    border=6,  # Tamaño del borde
)

qr.add_data(contenido)
qr.make(fit=True)

# Crear la imagen del QR
imagen = qr.make_image(fill_color="black", back_color="white")

# Guardar la imagen
imagen.save("codigo_qr.png")

print("¡Código QR generado y guardado como 'codigo_qr.png'!")

