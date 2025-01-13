from flask import jsonify, request
from app.models.file_model import FileModel

# Dados simulados
arquivos = [
    "arquivo1.txt",
    "arquivo2.txt"
]

dados_arquivos = list(
    map(
        lambda file_path: FileModel(caminho_original=file_path).gerar_dados(), arquivos
    )
)

def listar_arquivos():
    return jsonify([{"id": a.id, "nome": a.nome, "tamanho": a.tamanho} for a in arquivos])

def criar_arquivo():
    dados = request.json
    novo_arquivo = FileModel(len(arquivos) + 1, dados["nome"], dados["tamanho"])
    arquivos.append(novo_arquivo)
    return jsonify({"mensagem": "Arquivo criado!", "arquivo": vars(novo_arquivo)}), 201

def deletar_arquivo(id):
    global arquivos
    arquivos = [a for a in arquivos if a.id != id]
    return jsonify({"mensagem": f"Arquivo com ID {id} deletado"})
