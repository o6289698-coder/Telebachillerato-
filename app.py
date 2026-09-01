
import os
from flask import Flask, render_template, request, redirect, url_for
from google import genai

app = Flask(__name__)

# Configuración de la API de Google Gemini utilizando la variable de entorno
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = None
    if request.method == "POST":
        # Verificamos si la petición viene del chat con JavI.A.
        if "pregunta" in request.form:
            prompt = request.form.get("pregunta")
            if prompt:
                try:
                    # Llamada a la API utilizando el modelo actualizado
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                    respuesta_ia = response.text
                except Exception as e:
                    respuesta_ia = f"Error al conectar con JavI.A.: {str(e)}"

    return render_template("index.html", respuesta_ia=respuesta_ia)

if __name__ == "__main__":
    app.run(debug=True)
    
