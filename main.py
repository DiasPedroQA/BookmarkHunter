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


# main.py

# pylint: disable=C, E0401

# from flask import Flask
# from app.entrada_dados_web import json_frontend
# from app.routes.main_routes import bp as main_bp
# from app.controllers.analysis_controller import AnalysisController


# Inicializar controlador principal
# analysis_controller = AnalysisController()

# Dados simulados do frontend
# dados_processados = analysis_controller.processar_dados(json_frontend)

# print(f"Dados processados: {dados_processados}")


# def create_app():
#     """Fábrica para criar a instância do aplicativo Flask."""
#     flask_app = Flask(__name__)

#     # Registrar blueprints
#     flask_app.register_blueprint(main_bp, url_prefix="/analysis")

#     return flask_app


# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)


# def create_app():
#     """Fábrica para criar a instância do aplicativo Flask."""
#     flask_app = Flask(__name__)
#     flask_app.register_blueprint(path_bp, url_prefix="/paths")
#     return flask_app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)



# Exemplo de uso:
"""
Script para testar as classes FileRepository e FolderRepository.
"""

# pylint: disable=C, E0401

from pathlib import Path
from models.path_model import Arquivo, Diretorio
from repositories.file_repository import FileRepository
from repositories.folder_repository import FolderRepository


def testar_file_repository():
    """
    Testar métodos da classe FileRepository.
    """
    print("\n--- Testando FileRepository ---")

    # Mock de arquivos e diretórios
    arquivo_especifico = Path(
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html"
    )
    arquivo_renomeado = Path(
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024_renomeado.html"
    )
    diretorio_especifico = Path("/home/pedro-pm-dias/Downloads/Chrome/")
    novo_nome_diretorio = Path("/home/pedro-pm-dias/Downloads/Chrome/NovoDiretorio/")

    # Adicionar arquivos e diretórios simulados
    FileRepository.arquivos_virtuais.append(Arquivo(arquivo_especifico))
    FileRepository.diretorios_virtuais.append(Diretorio(diretorio_especifico))

    # Buscar um arquivo específico
    arquivo = FileRepository.buscar_arquivo(arquivo_especifico)
    if arquivo:
        print(f"Arquivo encontrado: {arquivo.para_json()}")

    # Buscar um diretório específico
    diretorio = FileRepository.buscar_diretorio(diretorio_especifico)
    if diretorio:
        print(f"Diretório encontrado: {diretorio.para_json()}")

    # Listar arquivos dentro de um diretório
    arquivos_encontrados = FileRepository.listar_arquivos(diretorio_especifico)
    for arquivo in arquivos_encontrados:
        print(f"Arquivo encontrado: {arquivo.para_json()}")

    # Listar arquivos com uma extensão específica
    arquivos_html = FileRepository.listar_arquivos_por_extensao(
        diretorio_especifico, ".html"
    )
    for arquivo in arquivos_html:
        print(f"Arquivo com extensão '.html': {arquivo.para_json()}")

    # Excluir um arquivo
    FileRepository.excluir_arquivo(arquivo_especifico)
    print(f"Arquivo {arquivo_especifico} excluído virtualmente.")

    # Renomear um arquivo
    FileRepository.renomear_arquivo(arquivo_especifico, arquivo_renomeado)
    print(f"Arquivo renomeado para: {arquivo_renomeado}")

    # Renomear um diretório
    FileRepository.renomear_diretorio(diretorio_especifico, novo_nome_diretorio)
    print(f"Diretório renomeado para: {novo_nome_diretorio}")


def testar_folder_repository():
    """
    Testar métodos da classe FolderRepository.
    """
    print("\n--- Testando FolderRepository ---")

    # Mock de diretórios
    diretorio = Path("/home/pedro-pm-dias/Downloads/Chrome/")
    subdiretorio_vazio = Path("/home/pedro-pm-dias/Downloads/Chrome/SubdiretorioVazio/")
    subdiretorio_com_arquivos = Path("/home/pedro-pm-dias/Downloads/Chrome/ComArquivos/")

    # Criar diretórios simulados
    FolderRepository.criar_diretorio(diretorio)
    FolderRepository.criar_diretorio(subdiretorio_vazio)
    FolderRepository.criar_diretorio(subdiretorio_com_arquivos)

    # Listar subdiretórios
    subdiretorios = FolderRepository.listar_subdiretorios(diretorio)
    for subdir in subdiretorios:
        print(f"Subdiretório encontrado: {subdir.caminho}")

    # Listar diretórios vazios
    diretorios_vazios = FolderRepository.listar_diretorios_vazios(diretorio)
    for vazio in diretorios_vazios:
        print(f"Diretório vazio encontrado: {vazio.caminho}")

    # Verificar existência de um diretório
    if FolderRepository.verificar_existencia_diretorio(diretorio):
        print(f"O diretório {diretorio} existe.")

    # Excluir um diretório
    FolderRepository.excluir_diretorio(subdiretorio_vazio)
    print(f"Diretório {subdiretorio_vazio} excluído.")

    # Excluir um diretório forçado
    FolderRepository.excluir_diretorio(subdiretorio_com_arquivos, forcar=True)
    print(f"Diretório {subdiretorio_com_arquivos} excluído forçadamente.")


if __name__ == "__main__":
    # Testar FileRepository
    testar_file_repository()

    # Testar FolderRepository
    testar_folder_repository()
