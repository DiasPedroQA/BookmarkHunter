# app/models/analisador_string.py
# pylint: disable=C, R, E, W

import sys
import os
import json
from typing import Optional, Dict, Union

# Caminho para a raiz do projeto (BookmarkHunter)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Importações
from app.services.path_services import (
    extrair_nome_item,
    extrair_pasta_mae,
    obter_permissoes_caminho,
)
from app.services.regex_services import (
    contar_diretorios,
    extrair_pasta_principal,
    sanitizar_caminho,
    validar_tamanho_nome_caminho,
    verificar_arquivo,
    verificar_caminho_absoluto,
    verificar_caminho_relativo,
)


class SanitizePath:

    def __init__(self, caminho_bruto: str):
        # Dados do objeto que serão criados
        self.caminho_original: str = caminho_bruto
        self.caminho_sanitizado: str
        self.formato_valido: bool
        self.eh_absoluto: bool
        self.eh_relativo: bool
        self.numero_diretorios: int
        self.permissoes: dict
        self.nome_item: Optional[str]
        self.pasta_principal: Optional[str]
        self.pasta_mae: Optional[str]
        self.eh_arquivo: bool
        self.eh_pasta: bool

        # Inicializa os atributos do objeto após a criação.
        self._processar_caminho()

    def _processar_caminho(self):
        """Processa e extrai informações do caminho."""
        self.caminho_sanitizado = sanitizar_caminho(self.caminho_original)
        self.formato_valido = validar_tamanho_nome_caminho(self.caminho_sanitizado)
        self.eh_absoluto = verificar_caminho_absoluto(self.caminho_sanitizado)
        self.eh_relativo = verificar_caminho_relativo(self.caminho_sanitizado)
        self.numero_diretorios = contar_diretorios(self.caminho_sanitizado)
        self.permissoes = obter_permissoes_caminho(self.caminho_sanitizado)
        self.nome_item = extrair_nome_item(self.caminho_sanitizado)
        self.pasta_principal = extrair_pasta_principal(self.caminho_sanitizado)
        self.pasta_mae = extrair_pasta_mae(self.caminho_sanitizado)
        self.eh_arquivo = verificar_arquivo(self.caminho_sanitizado)
        self.eh_pasta = not self.eh_arquivo

    def para_dict(self) -> Dict[str, Union[bool, int, None, str]]:
        """Converte os atributos do objeto para um dicionário."""
        return {
            "caminho_original": self.caminho_original,
            "caminho_sanitizado": self.caminho_sanitizado,
            "formato_valido": self.formato_valido,
            "eh_absoluto": self.eh_absoluto,
            "eh_relativo": self.eh_relativo,
            "permissoes": self.permissoes,
            "numero_diretorios": self.numero_diretorios,
            "nome_item": self.nome_item,
            "pasta_principal": self.pasta_principal,
            "pasta_mae": self.pasta_mae,
            "eh_arquivo": self.eh_arquivo,
            "eh_pasta": self.eh_pasta,
        }

    def gerar_json(self) -> str:
        """Gera uma representação JSON dos atributos do objeto."""
        return json.dumps(self.para_dict(), indent=4, ensure_ascii=False)


# # Exemplo de uso
# tipos_de_caminhos: Dict[str, str] = {
#     "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#     "Arquivo - Relativo e válido": "../imagens/foto.jpg",
#     "Arquivo - Absoluto e inválido": "/home/pedro-pm-dias/arquivo?*<>.html",
#     "Arquivo - Relativo e inválido": "../imagens/arquivo?*<>.jpg",
#     "Pasta - Absoluta e válida": "/home/pedro-pm-dias/Downloads/Chrome/",
#     "Pasta - Relativa e válida": "./Downloads/Chrome/",
#     "Pasta - Absoluta e inválida": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
#     "Pasta - Relativa e inválida": "./Downloads/Chrome/<>/",
# }

# for tipo, caminho in tipos_de_caminhos.items():
#     print(f"\nTipo do caminho: {tipo}")
#     caminho_obj = SanitizePath(caminho_bruto=caminho)
#     data = caminho_obj.gerar_json()
#     print(data)
