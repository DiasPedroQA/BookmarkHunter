# pylint: disable=C, R, E, W

from dataclasses import dataclass, field
import json
import re
from typing import Optional, Dict, Union


# Definição centralizada de expressões regulares
REGEX_CAMINHO_ABSOLUTO = r"^(?:[a-zA-Z]:\\|/home/[a-zA-Z0-9_-]+/)"
REGEX_CAMINHO_RELATIVO = r"^(?:\.{1,2}/)"
REGEX_NOME_ITEM = r"\.[a-zA-Z0-9]+$"
REGEX_SANITIZAR_CAMINHO = r"[^a-zA-Z0-9\- _./\\:]"
REGEX_EXTRAIR_PASTA = r"([^/\\]+)/[^/\\]+/?$"


@dataclass(init=True, repr=True, eq=True)
class SanitizePath:

    caminho_original: str
    caminho_sanitizado: str = field(init=False)
    formato_valido: bool = field(init=False)
    eh_absoluto: bool = field(init=False)
    eh_relativo: bool = field(init=False)
    numero_diretorios: int = field(init=False)
    nome_item: Optional[str] = field(init=False)
    pasta_principal: Optional[str] = field(init=False)
    pasta_mae: Optional[str] = field(init=False)
    eh_arquivo: bool = field(init=False)
    eh_pasta: bool = field(init=False)

    def __post_init__(self):
        """Inicializa os atributos do objeto após a criação."""
        self._inicializar_caminho()
        self._inicializar_informacoes()

    def _inicializar_caminho(self):
        """Sanitiza e valida o caminho original."""
        self.caminho_sanitizado = self._sanitizar_caminho(self.caminho_original)
        self.formato_valido = self._validar_tamanho_nome_caminho(
            self.caminho_sanitizado
        )

    def _inicializar_informacoes(self):
        """Extrai informações detalhadas do caminho sanitizado."""
        self.eh_absoluto = bool(
            re.match(REGEX_CAMINHO_ABSOLUTO, self.caminho_sanitizado)
        )
        self.eh_relativo = bool(
            re.match(REGEX_CAMINHO_RELATIVO, self.caminho_sanitizado)
        )
        self.numero_diretorios = self.caminho_sanitizado.count("/") - 1
        self.nome_item = self._extrair_nome_item(self.caminho_sanitizado)
        self.pasta_principal = self._extrair_pasta_principal(self.caminho_sanitizado)
        self.pasta_mae = self._extrair_pasta_mae(self.caminho_sanitizado)
        self.eh_arquivo = bool(re.search(REGEX_NOME_ITEM, self.caminho_sanitizado))
        self.eh_pasta = not self.eh_arquivo

    def _sanitizar_caminho(self, caminho: str) -> str:
        """Remove caracteres inválidos do caminho."""
        return re.sub(REGEX_SANITIZAR_CAMINHO, "", caminho).rstrip("/\\")

    def _validar_tamanho_nome_caminho(self, caminho: str) -> bool:
        """Valida o tamanho máximo permitido para o caminho."""
        if len(caminho) > 260:
            raise ValueError(
                f"O caminho '{caminho}' excede o limite de 260 caracteres."
            )
        return True

    def _extrair_nome_item(self, caminho: str) -> Optional[str]:
        """Extrai o nome do item (arquivo ou pasta) do caminho."""
        return caminho.split("/")[-1] if "/" in caminho else None

    def _extrair_pasta_principal(self, caminho: str) -> Optional[str]:
        """Extrai a pasta principal do caminho."""
        match = re.search(REGEX_EXTRAIR_PASTA, caminho)
        return match.group(1) if match else None

    def _extrair_pasta_mae(self, caminho: str) -> Optional[str]:
        """Extrai a pasta mãe do caminho."""
        partes = caminho.rstrip("/\\").split("/")
        return partes[-3] if len(partes) > 2 else None

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
