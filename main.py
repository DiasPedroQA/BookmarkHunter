# import os
# from flask import Flask, render_template
# from flask_cors import CORS
# from app.routes.bookmark_routes import bookmark_routes_bp

# # Criar a instância do Flask
# app = Flask(
#     __name__,
#     static_folder=os.path.join(
#         os.getcwd(), 'frontend/static'),  # Ajuste do caminho estático
#     template_folder=os.path.join(
#         os.getcwd(), 'frontend/templates')  # Ajuste do caminho dos templates
# )
# # Habilitar CORS para permitir requisições de qualquer origem
# CORS(app)

# # Registrar o blueprint de rotas relacionadas a bookmarks
# app.register_blueprint(bookmark_routes_bp, url_prefix="/bookmark")

# # Rota para renderizar a página principal
# @app.route("/")
# def home_page():
#     return render_template("index.html")

# # Rota para renderizar o arquivo de teste de bookmark
# @app.route("/test")
# def test_bookmark():
#     return render_template("test_bookmark.html")

# # Verificar se o script está sendo executado diretamente
# if __name__ == "__main__":
#     # Iniciar o servidor Flask no modo de depuração e especificar o host
#     app.run(debug=True, host="0.0.0.0", port=5000)


# main.py

"""
Este é o ponto de entrada da aplicação BookmarkHunter.

Ele inicializa uma instância do Flask, registra as rotas da bookmark por meio de blueprints 
e define um endpoint inicial para verificar o status da aplicação.
"""


from pathlib import Path


# Caminho para o arquivo HTML
file_path = Path("/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html")

# Criação de objetos para análise
analise = AnalisesHTML(file_path)
documento = HTMLDocument()

# Ler o conteúdo do arquivo
html_content = analise.ler_conteudo()

# Contar tags
contagem = analise.contar_tags(html_content, tags=["h3", "a"])
print(contagem)

# Extrair tags e adicionar ao objeto documento
tags_extraidas = analise.extrair_tags(html_content)
for tag in tags_extraidas:
    if isinstance(tag, H3Item):
        documento.add_h3_item(tag)
    elif isinstance(tag, AItem):
        documento.add_a_item(tag)

# Agora o objeto 'documento' contém os itens estruturados
print(f"H3 Items: {documento.h3_items}")
print(f"A Items: {documento.a_items}")
