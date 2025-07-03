let espectroInterval = null;

// Diccionario de traducción YOLO inglés -> español
const traduccionesYOLO = {
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
  "logo": "logotipo",
  // Agrega más según tus necesidades
};

// Validar usuario
async function validarUsuario() {
    const usuario = document.getElementById("usuario").value;
    const mensajeDiv = document.getElementById("mensaje-usuario");
    
    if (!usuario) {
        mensajeDiv.textContent = "Por favor, ingresa un usuario.";
        mensajeDiv.style.color = "red";
        return; // Detén la ejecución si el campo está vacío
    }
    try {
        const response = await fetch("/validar_usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario }),
        });

        const data = await response.json();
        mensajeDiv.textContent = data.mensaje;

        if (data.valido) {
            mensajeDiv.style.color = "green";
            document.getElementById("login").style.display = "none";
            document.getElementById("menu-modulos").style.display = "block";
            document.getElementById("modulo").style.display = "none";
            document.getElementById("modulo-video-voz").style.display = "none";
            document.getElementById("modulo-reconocimiento").style.display = "none";
            document.getElementById("ventana-respuesta").style.display = "none";
        } else {
            mensajeDiv.style.color = "red";
            document.getElementById("login").style.display = "none";
            document.getElementById("opciones-usuario-incorrecto").style.display = "block";
        }
    } catch (error) {
        mensajeDiv.textContent = "Error al validar el usuario.";
        mensajeDiv.style.color = "red";
    }
}

// Registrar usuario
async function registrarUsuario() {
    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const mensajeDiv = document.getElementById("mensaje-registro");

    try {
        const response = await fetch("/registrar_usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, correo }),
        });

        const data = await response.json();
        mensajeDiv.textContent = data.mensaje;
    } catch (error) {
        mensajeDiv.textContent = "Error al registrar el usuario.";
    }
}

// Volver a intentarlo
function volverAIntentarlo() {
    document.getElementById("opciones-usuario-incorrecto").style.display = "none";
    document.getElementById("login").style.display = "block";
}

// Mostrar formulario de registro
function mostrarRegistro() {
    document.getElementById("opciones-usuario-incorrecto").style.display = "none";
    document.getElementById("registro").style.display = "block";
}

// Usar reconocimiento facial (simulado)
function usarReconocimientoFacial() {
    const mensajeDiv = document.getElementById("mensaje-opciones");
    mensajeDiv.textContent = "Iniciando reconocimiento facial... (Pon tu cara frente a la cámara)";
    setTimeout(() => {
        mensajeDiv.textContent = "Reconocimiento facial exitoso. Bienvenido de nuevo.";
        mensajeDiv.style.color = "green";

         // Ocultar las opciones de usuario incorrecto
         document.getElementById("opciones-usuario-incorrecto").style.display = "none";

         // Mostrar el módulo de aprendizaje
         document.getElementById("modulo").style.display = "block";
    }, 3000); // Simula un retraso de 3 segundos
}
 
// Enviar pregunta al módulo de aprendizaje
async function enviarPregunta(pregunta) {
    // Elementos de la ventana independiente
    const respuestaDiv = document.querySelector("#ventana-respuesta #respuesta");
    const sujetoDiv = document.querySelector("#ventana-respuesta #sujeto-pregunta");
    const contenedorImagenes = document.querySelector("#ventana-respuesta #imagenes");

    respuestaDiv.textContent = "Cargando...";
    respuestaDiv.style.color = "blue";
    contenedorImagenes.innerHTML = "";

    const sujeto = extraerSujeto(pregunta);
    sujetoDiv.textContent = sujeto.charAt(0).toUpperCase() + sujeto.slice(1);

    try {
        const response = await fetch("/modulo_aprendizaje", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta }),
        });

        const data = await response.json();
        if (response.ok) {
            respuestaDiv.textContent = data.respuesta;
            respuestaDiv.style.color = "black";

            if (data.imagenes && data.imagenes.length > 0) {
                data.imagenes.forEach((url) => {
                    const img = document.createElement("img");
                    img.src = url;
                    img.alt = "Imagen relacionada";
                    img.style.width = "200px";
                    img.style.margin = "10px";
                    contenedorImagenes.appendChild(img);
                });
            } else {
                respuestaDiv.textContent += " (No se encontraron imágenes relacionadas)";
            }
        } else {
            respuestaDiv.textContent = data.error;
            respuestaDiv.style.color = "red";
        }
    } catch (error) {
        respuestaDiv.textContent = "Error al enviar la pregunta.";
        respuestaDiv.style.color = "red";
    }
}

// Suponiendo que tienes una función como esta para mostrar la respuesta:
function mostrarRespuesta(texto, imagenes) {
    document.getElementById("respuesta").innerHTML = texto;
    // ...código para mostrar imágenes...
    document.getElementById("respuesta-contenedor").style.display = "flex";
}

// Validar el formulario de preguntas
document.getElementById("formulario").addEventListener("submit", function (e) {
    e.preventDefault();
    const pregunta = document.getElementById("pregunta").value.trim();
    if (!pregunta) {
        alert("Por favor, ingresa una pregunta.");
        return;
    }
    enviarPregunta(pregunta);
    document.getElementById("modulo").style.display = "none";
    document.getElementById("ventana-respuesta").style.display = "block";
    document.getElementById("modulo-video-voz").style.display = "none";
});

function extraerSujeto(pregunta) {
    // Elimina signos y stopwords básicos
    const stopwords = ["qué", "es", "un", "una", "de", "la", "el", "los", "las", "por", "para", "con", "y", "o", "a", "en", "que", "cómo", "?", "¿"];
    let palabras = pregunta.toLowerCase().replace(/[¿?]/g, '').split(' ');
    palabras = palabras.filter(p => !stopwords.includes(p));
    return palabras.length > 0 ? palabras.join(' ') : pregunta;
}

// --- Módulo de consulta por voz y video ---
const btnVoz = document.getElementById('btn-voz');
const textoVoz = document.getElementById('texto-voz');
const videoRespuesta = document.getElementById('video-respuesta');

if (btnVoz) {
    let recognition;
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.continuous = false;

        btnVoz.onclick = () => {
            recognition.start();
            textoVoz.textContent = "Escuchando...";
        };

        recognition.onresult = (event) => {
            const consulta = event.results[0][0].transcript;
            textoVoz.textContent = consulta;
            // Aquí puedes hacer una consulta al backend para buscar un video real
            mostrarVideoDemo(consulta);
        };

        recognition.onerror = () => {
            textoVoz.textContent = "No se pudo reconocer la voz.";
        };
    } else {
        btnVoz.disabled = true;
        textoVoz.textContent = "Reconocimiento de voz no soportado en este navegador.";
    }

    // Demo: muestra un video de YouTube según la consulta (puedes personalizar)
    async function mostrarVideoDemo(consulta) {
        document.getElementById("modulo").style.display = "none";
        document.getElementById("modulo-video-voz").style.display = "block";
        const query = encodeURIComponent(consulta);

        // Tu API Key de YouTube
        const API_KEY = "AIzaSyByCwvkyio-NmNea9dnaUUujPbZT0jRyBw"; // <-- Pega aquí tu API Key

        // Llama a la API de YouTube para buscar el primer video
        const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&q=${query}&key=${API_KEY}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            if (data.items && data.items.length > 0) {
                const videoId = data.items[0].id.videoId;
                document.getElementById("video-respuesta").innerHTML = `
                    <iframe width="400" height="225" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen></iframe>
                    <p>Consulta: ${consulta}</p>
                `;
            } else {
                document.getElementById("video-respuesta").innerHTML = `
                    <p>No se encontró un video relacionado.</p>
                    <p>Consulta: ${consulta}</p>
                `;
            }
        } catch (error) {
            document.getElementById("video-respuesta").innerHTML = `
                <p>Error al buscar el video.</p>
                <p>Consulta: ${consulta}</p>
            `;
        }
    }
}



// Mostrar módulo de consulta tradicional
document.getElementById("ir-a-consulta").onclick = function() {
    document.getElementById("menu-modulos").style.display = "none";
    document.getElementById("modulo").style.display = "block";
    document.getElementById("modulo-video-voz").style.display = "none";
    document.getElementById("modulo-reconocimiento").style.display = "none";
    document.getElementById("ventana-respuesta").style.display = "none";
};

// Mostrar módulo de voz/video
document.getElementById("ir-a-voz").onclick = function() {
    document.getElementById("menu-modulos").style.display = "none";
    document.getElementById("modulo").style.display = "none";
    document.getElementById("modulo-video-voz").style.display = "block";
    document.getElementById("modulo-reconocimiento").style.display = "none";
    document.getElementById("ventana-respuesta").style.display = "none";
};

// Mostrar módulo de reconocimiento
document.getElementById("ir-a-reconocimiento").onclick = function() {
    document.getElementById("menu-modulos").style.display = "none";
    document.getElementById("modulo").style.display = "none";
    document.getElementById("modulo-video-voz").style.display = "none";
    document.getElementById("modulo-reconocimiento").style.display = "block";
    document.getElementById("ventana-respuesta").style.display = "none";
};

// Vista previa de imagen
document.getElementById("input-imagen").addEventListener("change", function(e) {
    const file = e.target.files[0];
    const preview = document.getElementById("preview-imagen");
    if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
            preview.innerHTML = `<img src="${evt.target.result}" alt="Vista previa" style="max-width:200px;">`;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = "";
    }
});

// Enviar imagen al backend para reconocimiento
document.getElementById("btn-reconocer").onclick = async function() {
    const fileInput = document.getElementById("input-imagen");
    if (!fileInput.files[0]) {
        alert("Por favor, selecciona una imagen.");
        return;
    }
    const formData = new FormData();
    formData.append("imagen", fileInput.files[0]);
    try {
        const response = await fetch("/reconocer_imagen", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        const archivo = fileInput.files[0];
        if (data.descripcion) {
            // Usa los objetos detectados, no la descripción
            if (data.objetos && data.objetos.length > 0) {
                const relacionadas = data.objetos.map(objeto => buscarImagenRelacionada(objeto));
                mostrarModal(
                    URL.createObjectURL(archivo),
                    relacionadas,
                    descripcionExplicativa(data.objetos.join(', '))
                );
            } else {
                mostrarModal(
                    URL.createObjectURL(archivo),
                    [],
                    "No se detectaron objetos en la imagen."
                );
            }
        } else if (data.error) {
            mostrarModal(
                URL.createObjectURL(archivo),
                [
                    buscarImagenRelacionada('error'),
                    buscarImagenRelacionada('error')
                ],
                "No se pudo procesar la imagen."
            );
        }
    } catch (error) {
        mostrarModal(
            "",
            [buscarImagenRelacionada('error'), buscarImagenRelacionada('error')],
            "Error al procesar la imagen."
        );
    }
}

// Manejar clics en los iconos de volver
document.addEventListener("click", function(e) {
    // Si el clic fue en el botón de volver del registro
    if (e.target.closest('#volver-registro')) {
        document.getElementById("registro").style.display = "none";
        document.getElementById("login").style.display = "block";
        document.getElementById("menu-modulos").style.display = "none";
        document.getElementById("modulo").style.display = "none";
        document.getElementById("modulo-reconocimiento").style.display = "none";
        document.getElementById("modulo-video-voz").style.display = "none";
        document.getElementById("ventana-respuesta").style.display = "none";
        return; // ¡Esto es clave! Así no se ejecuta el listener global
    }

    // Listener global para otros iconos de volver
    if (e.target.closest('.icono-volver')) {
        document.getElementById("modulo").style.display = "none";
        document.getElementById("modulo-video-voz").style.display = "none";
        document.getElementById("modulo-reconocimiento").style.display = "none";
        document.getElementById("ventana-respuesta").style.display = "none";
        document.getElementById("menu-modulos").style.display = "block";
    }
});

document.getElementById("volver-consulta").onclick = function() {
    document.getElementById("ventana-respuesta").style.display = "none";
    document.getElementById("modulo").style.display = "block";
};

function mostrarDescripcion(texto) {
  document.getElementById('descripcion').innerText = texto;
  document.getElementById('descripcion-container').style.display = 'flex';
}

function ocultarDescripcion() {
  document.getElementById('descripcion-container').style.display = 'none';
}

function leerDescripcion() {
  const descripcion = document.getElementById('descripcion').innerText;
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(descripcion);
    utter.lang = 'es-ES';
    window.speechSynthesis.speak(utter);
  } else {
    alert('Tu navegador no soporta síntesis de voz.');
  }
}

// Ejemplo de integración con tu fetch:
document.getElementById('formulario-imagen').onsubmit = function(e) {
  e.preventDefault();
  ocultarDescripcion(); // Oculta antes de enviar
  // ... tu código para enviar la imagen ...
  fetch('/reconocer_imagen', { /* ... */ })
    .then(res => res.json())
    .then(data => {
      if (data.descripcion) {
        mostrarDescripcion(data.descripcion);
      } else if (data.error) {
        mostrarDescripcion(data.error);
      }
    });
};

// Mostrar el modal con la imagen principal, relacionadas y descripción
function mostrarModal(imagenPrincipal, relacionadas, descripcion) {
  document.getElementById('img-principal').src = imagenPrincipal;
  document.getElementById('img-relacionada-1').src = relacionadas[0];
  document.getElementById('img-relacionada-2').src = relacionadas[1];
  document.getElementById('descripcion-modal').innerText = descripcion;
  document.getElementById('modal-resultado').style.display = 'flex';
  limpiarEspectro();
}

function cerrarModal() {
  document.getElementById('modal-resultado').style.display = 'none';
  window.speechSynthesis.cancel();
  limpiarEspectro();
}

function leerDescripcionModal() {
  const descripcion = document.getElementById('descripcion-modal').innerText;
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(descripcion);
    utter.lang = 'es-ES';
    utter.onstart = animarEspectro;
    utter.onend = limpiarEspectro;
    window.speechSynthesis.speak(utter);
  }
}
// Animación del espectro de audio
function animarEspectro() {
  const canvas = document.getElementById('canvas-espectro');
  const ctx = canvas.getContext('2d');
  espectroInterval = setInterval(() => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < 20; i++) {
      const altura = Math.random() * canvas.height;
      ctx.fillStyle = '#4B0082';
      ctx.fillRect(i * 11, canvas.height - altura, 8, altura);
    }
  }, 80);
}
function limpiarEspectro() {
  clearInterval(espectroInterval);
  const canvas = document.getElementById('canvas-espectro');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}


function buscarImagenRelacionada(concepto) {
  // Traduce el concepto si existe en el diccionario
  const conceptoTraducido = traduccionesYOLO[concepto] || concepto;
  // Usa Unsplash con el concepto traducido
  return `https://source.unsplash.com/80x80/?${encodeURIComponent(conceptoTraducido)}`;
}

function descripcionExplicativa(descripcion) {
  const conceptos = descripcion.split(',').map(c => c.trim());
  if (conceptos.length === 0 || !conceptos[0]) return "No se detectaron objetos en la imagen.";

  if (conceptos.length === 1) {
    return `La imagen parece mostrar principalmente un(a) ${conceptos[0]}.`;
  } else if (conceptos.length === 2) {
    return `En la imagen se pueden observar un(a) ${conceptos[0]} y un(a) ${conceptos[1]}.`;
  } else {
    return `La imagen contiene principalmente: ${conceptos.slice(0, -1).join(', ')}y ${conceptos[conceptos.length - 1]}.`;
  }
}

// Volver a la pantalla de registro
document.addEventListener("DOMContentLoaded", function() {
  const volverRegistro = document.getElementById("volver-registro");
  if (volverRegistro) {
    volverRegistro.addEventListener("click", function(e) {
      e.stopPropagation();
      document.getElementById("registro").style.display = "none";
      document.getElementById("login").style.display = "block";
      document.getElementById("menu-modulos").style.display = "none";
      document.getElementById("modulo").style.display = "none";
      document.getElementById("modulo-reconocimiento").style.display = "none";
      document.getElementById("modulo-video-voz").style.display = "none";
      document.getElementById("ventana-respuesta").style.display = "none";
    });
  }
});

// Supón que 'data' es la respuesta del backend
const contenedorImagenes = document.getElementById("imagenes-relacionadas");
contenedorImagenes.innerHTML = ""; // Limpia antes

if (data.objetos && data.objetos.length > 0) {
  data.objetos.forEach(objeto => {
    const img = document.createElement("img");
    img.src = buscarImagenRelacionada(objeto);
    img.alt = objeto;
    img.width = 80;
    img.height = 80;
    contenedorImagenes.appendChild(img);
  });
}

// Nueva funcionalidad: Dactilografía
document.getElementById("btn-dactilar").onclick = async function() {
    const mensaje = document.getElementById("mensaje-dactilar");
    mensaje.textContent = "";
    if (!window.PublicKeyCredential) {
        mensaje.textContent = "Tu navegador no soporta autenticación biométrica.";
        return;
    }
    try {
        // Solicita autenticación biométrica (huella, rostro, PIN, etc.)
        await navigator.credentials.get({
            publicKey: {
                challenge: new Uint8Array(32), // Solo para demo, en producción debe venir del backend
                timeout: 60000,
                userVerification: "required"
            }
        });
        mensaje.textContent = "¡Huella digital verificada!";
        mensaje.style.color = "green";
        // Aquí puedes continuar con el flujo de validación de usuario
    } catch (e) {
        mensaje.textContent = "No se pudo verificar la huella digital o fue cancelado.";
        mensaje.style.color = "red";
    }
};