# main.py
"""
Este é o ponto de entrada da aplicação BookmarkHunter.

Ele inicializa uma instância do Flask, registra as rotas da bookmark por meio de blueprints 
e define um endpoint inicial para verificar o status da aplicação.
"""

import os
from flask import Flask, render_template
from flask_cors import CORS
from app.routes.bookmark_routes import bookmark_routes_bp

# Criar a instância do Flask
app = Flask(
    __name__,
    static_folder=os.path.join(
        os.getcwd(), 'frontend/static'),  # Ajuste do caminho estático
    template_folder=os.path.join(
        os.getcwd(), 'frontend/templates')  # Ajuste do caminho dos templates
)
# Habilitar CORS para permitir requisições de qualquer origem
CORS(app)

# Registrar o blueprint de rotas relacionadas a bookmarks
app.register_blueprint(bookmark_routes_bp, url_prefix="/bookmark")

# Rota para renderizar a página principal
@app.route("/")
def home_page():
    return render_template("index.html")

# Rota para renderizar o arquivo de teste de bookmark
@app.route("/test")
def test_bookmark():
    return render_template("test_bookmark.html")

# Verificar se o script está sendo executado diretamente
if __name__ == "__main__":
    # Iniciar o servidor Flask no modo de depuração e especificar o host
    app.run(debug=True, host="0.0.0.0", port=5000)
