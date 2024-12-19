"""
Este é o ponto de entrada da aplicação BookmarkHunter.

Ele inicializa uma instância do Flask, registra as rotas da API por meio de blueprints 
e define um endpoint inicial para verificar o status da aplicação.
"""

# Importação da biblioteca Flask
from flask import Flask
# Importar o blueprint de rotas relacionadas a arquivos
from app.routes.file_routes import file_routes_bp

# Criar a instância do Flask no arquivo main.py
app = Flask(__name__)

# Registrar o blueprint de rotas com um prefixo de URL "/api"
app.register_blueprint(file_routes_bp, url_prefix="/api")

# Verificar se o script está sendo executado diretamente
if __name__ == "__main__":
    # Iniciar o servidor Flask no modo de depuração
    app.run(debug=True)
