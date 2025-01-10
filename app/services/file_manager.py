# pylint: disable=C

import os
import json
from GitHub.Kabalah.flask_api_mvc.app.entrada_dados_web import filtrar_caminhos_validos

# app/services/file_manager.py
import os

class FileManager:
    def gerar_log(self, resultados):
        log_path = os.path.join(os.getcwd(), "analysis.log")
        with open(log_path, "w") as log_file:
            for resultado in resultados:
                log_file.write(f"{resultado}\n")
        return log_path
# app/repositories/file_repository.py
import os
import json

class FileRepository:
    def salvar_json(self, resultados):
        json_path = os.path.join(os.getcwd(), "analysis.json")
        with open(json_path, "w") as json_file:
            json.dump(resultados, json_file, indent=4, ensure_ascii=False)
        return json_path

class FileManager:
    """Gerenciador de arquivos"""

    @staticmethod
    def carregar_dados_json(json_dados):
        """Carrega e decodifica os dados JSON"""
        return json.loads(json_dados).get("jsonEntrada", [])

    @staticmethod
    def filtrar_caminhos(caminhos):
        """Filtra os caminhos válidos"""
        return filtrar_caminhos_validos(caminhos)


def validate_path(path):
    """Verifica se o caminho existe"""
    return os.path.exists(path)


def analyze_paths(paths):
    """
    Analisa uma lista de caminhos.
    :param paths: list[str]
    :return: list[dict]
    """
    results = []
    for path in paths:
        if os.path.exists(path):
            result = {
                "path": path,
                "exists": True,
                "is_file": os.path.isfile(path),
                "is_dir": os.path.isdir(path),
            }
            if result["is_file"]:
                result["size"] = os.path.getsize(path)
            results.append(result)
        else:
            results.append({"path": path, "exists": False})
    return results
