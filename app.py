import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configuración con la librería clásica y directa
genai.configure(api_key="AQ.Ab8RN6lHQ1MKtGrxq5CPm02Zp6eLijL5t0vbAHtwe9SUWMfJw")

# Usamos el modelo estable
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta_ia = None
    if request.method == "POST":
        prompt = request.form.get("pregunta")
        if prompt:
            try:
                response = model.generate_content(prompt)
                respuesta_ia = response.text
            except Exception as e:
                respuesta_ia = f"Error al conectar con JavI.A.: {str(e)}"

    return render_template("index.html", respuesta_ia=respuesta_ia)

if __name__ == "__main__":
    app.run(debug=True)
    
