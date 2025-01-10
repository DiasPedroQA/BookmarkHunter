import json
from typing import List
from app.repositories.path_repository import PathRepository
from GitHub.Kabalah.flask_api_mvc.app.models.path_model2 import Arquivo, Diretorio


class PathService:
    """Serviço para processar caminhos de arquivos e diretórios."""

    def __init__(self):
        self.repository = PathRepository()

    def processar_caminhos(self, json_bruto: str) -> List[dict]:
        """Processa os caminhos fornecidos, criando objetos Arquivo ou Diretorio."""
        try:
            json_entrada = json.loads(json_bruto)
            if not self.repository.validar_json(json_entrada):
                raise ValueError("Estrutura JSON inválida.")
        except json.JSONDecodeError as e:
            raise ValueError("Entrada JSON inválida.") from e

        lista_caminhos = json_entrada["jsonEntrada"]
        caminhos_ajustados = self.repository.ajustar_caminhos(lista_caminhos)

        resultados_processados = []
        for caminho in caminhos_ajustados:
            if caminho.is_file():
                resultados_processados.append(Arquivo(caminho).para_json())
            elif caminho.is_dir():
                resultados_processados.append(Diretorio(caminho).para_json())
            else:
                resultados_processados.append(
                    {"caminho": str(caminho), "erro": "Caminho inválido"}
                )
        return resultados_processados


# app/services/path_service.py
from GitHub.Kabalah.flask_api_mvc.app.models.path_model2 import AnalisadorCaminhos
from app.repositories.file_repository import FileRepository
from app.services.file_manager import FileManager


class PathService:
    def __init__(self):
        self.analisador = AnalisadorCaminhos()
        self.file_manager = FileManager()
        self.file_repository = FileRepository()

    def analisar_caminhos(self, dados_entrada):
        """
        Analisa os caminhos recebidos, criando arquivos de log e JSON.
        """
        # Processar caminhos
        resultados = self.analisador.processar_caminhos(dados_entrada)

        # Gerar arquivos de log e JSON
        log_path = self.file_manager.gerar_log(resultados)
        json_path = self.file_repository.salvar_json(resultados)

        return {"log_path": log_path, "json_path": json_path}
