# pylint: disable=C, R, E, W

# from dataclasses import dataclass, field
# import json
# import os
# from pathlib import Path
# from typing import Dict, Union
# from analisador_string import SanitizePath


# @dataclass(init=True, repr=True, eq=True)
# class PathlibCaminho:
#     """
#     Representa os dados de um caminho após análise e sanitização.
#     """

#     caminho_original: str
#     caminho_existe: bool = field(init=False)
#     tamanho_em_bytes: int = field(init=False, default=0)
#     data_criacao: float = field(init=False, default=0.0)
#     data_modificacao: float = field(init=False, default=0.0)
#     data_acesso: float = field(init=False, default=0.0)
#     permissao_leitura: bool = field(init=False)
#     permissao_escrita: bool = field(init=False)
#     permissao_execucao: bool = field(init=False)

#     def __post_init__(self):
#         if not isinstance(self.caminho_original, str) or not self.caminho_original:
#             raise ValueError("O caminho fornecido deve ser uma string não vazia.")

#     def verificar_se_caminho_existe(self):
#         caminho = Path(self.caminho_original)
#         self.caminho_existe = caminho.exists()

#     def definir_metadados(self):
#         caminho = Path(self.caminho_original)
#         if caminho.exists():
#             estatisticas = caminho.stat()
#             self.tamanho_em_bytes = estatisticas.st_size
#             self.data_criacao = estatisticas.st_ctime
#             self.data_modificacao = estatisticas.st_mtime
#             self.data_acesso = estatisticas.st_atime

#     def definir_permissoes(self):
#         caminho = Path(self.caminho_original)
#         self.permissao_leitura = os.access(self.caminho_original, os.R_OK)
#         self.permissao_escrita = os.access(self.caminho_original, os.W_OK)
#         self.permissao_execucao = os.access(self.caminho_original, os.X_OK)

#     def obter_informacoes(self) -> Dict[str, Union[bool, int, float]]:
#         objeto_caminho = SanitizePath(caminho_original=self.caminho_original)
#         if not objeto_caminho.formato_valido:
#             raise ValueError(f"O caminho '{self.caminho_original}' não é válido.")

#         json_objeto_caminho: Dict[str, Union[bool, int, None, str]] = json.loads(
#             objeto_caminho.gerar_json()
#         )

#         self.verificar_se_caminho_existe()
#         self.definir_metadados()
#         self.definir_permissoes()

#         dados_novos = {
#             "caminho_original": objeto_caminho.caminho_original,
#             "caminho_existe": self.caminho_existe,
#             "tamanho_em_bytes": self.tamanho_em_bytes,
#             "data_criacao": self.data_criacao,
#             "data_modificacao": self.data_modificacao,
#             "data_acesso": self.data_acesso,
#             "permissao_leitura": self.permissao_leitura,
#             "permissao_escrita": self.permissao_escrita,
#             "permissao_execucao": self.permissao_execucao,
#         }

#         json_objeto_caminho.update(dados_novos)
#         return json_objeto_caminho


# Exemplo de uso
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
#     caminho_obj = PathlibCaminho(caminho_original=caminho)
#     data = caminho_obj.obter_informacoes()
#     print(caminho, "=>", data)
