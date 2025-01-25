# pylint: disable=C, R, E, W

import json
import re
from typing import Optional, Dict, Union
from app.services.path_services import (
    sanitizar_caminho,
    validar_tamanho_nome_caminho,
    verificar_caminho_absoluto,
    verificar_caminho_relativo,
    contar_diretorios,
    extrair_nome_item,
    extrair_pasta_principal,
    extrair_pasta_mae,
    verificar_arquivo,
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
#     caminho_obj = SanitizePath(caminho_original=caminho)
#     data = caminho_obj.gerar_json()
#     print(data)


# # Tipo do caminho: Arquivo - Absoluto e válido
# {
#     'caminho_original': '/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html',
#     'caminho_sanitizado': '/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html',
#     'formato_valido': True,
#     'eh_absoluto': True,
#     'eh_relativo': False,
#     'numero_diretorios': 4,
#     'nome_item': 'favoritos_23_12_2024.html',
#     'pasta_principal': 'Chrome',
#     'pasta_mae': 'Downloads',
#     'eh_arquivo': True,
#     'eh_pasta': False
# }

# # Tipo do caminho: Arquivo - Relativo e válido
# {
#     'caminho_original': '../imagens/foto.jpg',
#     'caminho_sanitizado': '../imagens/foto.jpg',
#     'formato_valido': True,
#     'eh_absoluto': False,
#     'eh_relativo': True,
#     'numero_diretorios': 1,
#     'nome_item': 'foto.jpg',
#     'pasta_principal': 'imagens',
#     'pasta_mae': '..',
#     'eh_arquivo': True,
#     'eh_pasta': False
# }

# # Tipo do caminho: Arquivo - Absoluto e inválido
# {
#     'caminho_original': '/home/pedro-pm-dias/arquivo?*<>.html', 'caminho_sanitizado': '/home/pedro-pm-dias/arquivo.html', 'formato_valido': True, 'eh_absoluto': True, 'eh_relativo': False, 'numero_diretorios': 2, 'nome_item': 'arquivo.html', 'pasta_principal': 'pedro-pm-dias', 'pasta_mae': 'home', 'eh_arquivo': True, 'eh_pasta': False}

# # Tipo do caminho: Arquivo - Relativo e inválido
# {
#     'caminho_original': '../imagens/arquivo?*<>.jpg',
#     'caminho_sanitizado': '../imagens/arquivo.jpg',
#     'formato_valido': True,
#     'eh_absoluto': False,
#     'eh_relativo': True,
#     'numero_diretorios': 1,
#     'nome_item': 'arquivo.jpg',
#     'pasta_principal': 'imagens',
#     'pasta_mae': '..',
#     'eh_arquivo': True,
#     'eh_pasta': False
# }

# # Tipo do caminho: Pasta - Absoluta e válida
# {
#     'caminho_original': '/home/pedro-pm-dias/Downloads/Chrome/',
#     'caminho_sanitizado': '/home/pedro-pm-dias/Downloads/Chrome',
#     'formato_valido': True,
#     'eh_absoluto': True,
#     'eh_relativo': False,
#     'numero_diretorios': 3,
#     'nome_item': 'Chrome',
#     'pasta_principal': 'Downloads',
#     'pasta_mae': 'pedro-pm-dias',
#     'eh_arquivo': False,
#     'eh_pasta': True
# }

# # Tipo do caminho: Pasta - Relativa e válida
# {
#     'caminho_original': './Downloads/Chrome/',
#     'caminho_sanitizado': './Downloads/Chrome',
#     'formato_valido': True,
#     'eh_absoluto': False, 'eh_relativo': True,
#     'numero_diretorios': 1,
#     'nome_item': 'Chrome',
#     'pasta_principal': 'Downloads',
#     'pasta_mae': '.',
#     'eh_arquivo': False,
#     'eh_pasta': True
# }

# # Tipo do caminho: Pasta - Absoluta e inválida
# {
#     'caminho_original': '/home/pedro-pm-dias/Downloads/Chrome/<>/',
#     'caminho_sanitizado': '/home/pedro-pm-dias/Downloads/Chrome',
#     'formato_valido': True,
#     'eh_absoluto': True,
#     'eh_relativo': False,
#     'numero_diretorios': 3, 'nome_item': 'Chrome',
#     'pasta_principal': 'Downloads',
#     'pasta_mae': 'pedro-pm-dias',
#     'eh_arquivo': False,
#     'eh_pasta': True
# }

# # Tipo do caminho: Pasta - Relativa e inválida
# {
#     'caminho_original': './Downloads/Chrome/<>/',
#     'caminho_sanitizado': './Downloads/Chrome',
#     'formato_valido': True,
#     'eh_absoluto': False,
#     'eh_relativo': True,
#     'numero_diretorios': 1,
#     'nome_item': 'Chrome',
#     'pasta_principal': 'Downloads',
#     'pasta_mae': '.',
#     'eh_arquivo': False,
#     'eh_pasta': True
# }
