import os
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Configuración de la API usando directamente la llave nueva
client = genai.Client(api_key="AQ.Ab8RN6lHQ1MKtGrxq5CPm02Zp6eLijL5t0vbAHtwe9SUWMfJw")

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = None
    if request.method == "POST":
        prompt = request.form.get("pregunta")
        if prompt:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                respuesta_ia = response.text
            except Exception as e:
                respuesta_ia = f"Error al conectar con JavI.A.: {str(e)}"

    return render_template("index.html", respuesta_ia=respuesta_ia)

if __name__ == "__main__":
    app.run(debug=True)
    
