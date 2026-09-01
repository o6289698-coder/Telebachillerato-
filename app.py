import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from google import genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html', respuesta_ia=None)

@app.route('/procesar', methods=['POST'])
def procesar():
    accion = request.form.get('accion')
    
    if accion == 'preguntar_ia':
        pregunta_usuario = request.form.get('pregunta_ia', '').strip()
        if not pregunta_usuario:
            return render_template('index.html', respuesta_ia="Por favor escribe una duda o pregunta.")
        
        try:
            prompt_sistema = (
                "Eres JavI.A., un asesor académico virtual amable y claro, diseñado para ayudar "
                "a estudiantes de preparatoria del Telebachillerato Comunitario San Javier. "
                "Explica los temas de forma sencilla, educativa y motivadora."
            )
            
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=f"{prompt_sistema}\n\nPregunta del alumno: {pregunta_usuario}"
            )
            respuesta_texto = response.text
        except Exception as e:
            respuesta_texto = f"Lo siento, hubo un error al conectar con JavI.A. Asegúrate de configurar la llave de API en Render. (Detalle: {str(e)})"
            
        return render_template('index.html', respuesta_ia=respuesta_texto, pregunta_anterior=pregunta_usuario)

    if accion == 'texto_a_pdf':
        titulo = request.form.get('titulo_documento', 'Documento')
        return f"Texto recibido para generar PDF con el título: '{titulo}'."

    if 'archivo' not in request.files:
        return redirect(url_for('index'))
    
    archivo = request.files['archivo']
    if archivo.filename == '':
        return redirect(url_for('index'))
    
    if archivo:
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(filepath)
        
        return f"Archivo {filename} recibido correctamente para la acción: {accion}."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  
