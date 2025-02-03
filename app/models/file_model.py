# # app/models/file_model.py
# # pylint: disable=C, R, E, W

# """
# Módulo de Modelo de Arquivo para manipulação de operações com arquivos.

# Este módulo fornece funcionalidades para gerenciar armazenamento e recuperação 
# de dados baseados em arquivo. Inclui utilitários para trabalhar com arquivos JSON, 
# manipulação de caminhos e operações no sistema de arquivos.

# Classes:
#     FileModel: Gerencia operações de arquivo e persistência de dados

# Funções:
#     Nenhuma

# Constantes:
#     Nenhuma

# Dependências:
#     - json: Para serialização/desserialização de dados JSON
#     - os: Para funcionalidades dependentes do sistema operacional
#     - pathlib.Path: Para caminhos do sistema de arquivos orientados a objeto
#     - typing: Para dicas de tipo (List, Dict, Optional)
# """

# import sys
# import json
# from pathlib import Path
# from typing import Dict, List, Optional, Union
# from os import stat_result, access, R_OK, W_OK, X_OK
# from favorite_model import HtmlTag

# # Obtém o diretório raiz do projeto
# project_root = Path(__file__).resolve().parent.parent
# sys.path.append(str(project_root))

# from app.services.global_services import GeneralServices


# class InformacoesCaminho:
#     """
#     A classe `InformacoesCaminho` fornece métodos para manipulação e
#     obtenção de informações sobre caminhos de arquivos e diretórios.
#     """

#     def __init__(self, caminho_string: str):
#         """
#         Inicializa a instância com um caminho fornecido e verifica se ele existe.

#         Args:
#             caminho_string (str): Caminho do arquivo ou diretório.
#         """
#         self.caminho = Path(caminho_string)
#         self.conversores = GeneralServices()
#         self.tag_model = HtmlTag()
#         if not self.caminho.exists():
#             raise FileNotFoundError(f"O caminho '{caminho_string}' não existe.")

#     @staticmethod
#     def nomenclatura(caminho: Path) -> Dict[str, str]:
#         """Retorna informações sobre o nome, extensões, diretório pai e partes do caminho."""
#         return {
#             "nome_puro": caminho.stem,
#             "extensoes": caminho.suffixes,
#             "pai": str(caminho.parent),
#             "raiz": caminho.root,
#             "partes": list(caminho.parts),
#             "caminho_absoluto": str(caminho.absolute()),
#             "caminho_resolvido": str(caminho.resolve()),
#         }

#     @staticmethod
#     def validar_caminho(caminho: Path) -> Dict[str, bool]:
#         """Retorna um dicionário com validações sobre o caminho."""
#         return {
#             "eh_absoluto": "Sim" if caminho.is_absolute() else "Não",
#             "eh_arquivo": "Sim" if caminho.is_file() else "Não",
#             "eh_diretorio": "Sim" if caminho.is_dir() else "Não",
#             "existe": "Sim" if caminho.exists() else "Não",
#             "eh_link_simbolico": "Sim" if caminho.is_symlink() else "Não",
#         }

#     @staticmethod
#     def verificar_permissoes(caminho: Path) -> Dict[str, bool]:
#         """Verifica as permissões de leitura, escrita e execução."""
#         return {
#             "leitura": "Sim" if access(caminho, R_OK) else "Não",
#             "escrita": "Sim" if access(caminho, W_OK) else "Não",
#             "execucao": "Sim" if access(caminho, X_OK) else "Não",
#         }

#     def obter_estatisticas(self, caminho: Path) -> Dict[str, float]:
#         """Retorna estatísticas sobre o arquivo ou diretório."""
#         estatisticas: stat_result = caminho.stat()
#         return {
#             "tamanho": self.conversores.converter_tamanho(estatisticas.st_size),
#             "data_criacao": self.conversores.converter_timestamp(estatisticas.st_ctime),
#             "data_modificacao": self.conversores.converter_timestamp(
#                 estatisticas.st_mtime
#             ),
#             "data_acesso": self.conversores.converter_timestamp(estatisticas.st_atime),
#         }

#     def obter_informacoes(self) -> Dict:
#         """Retorna um dicionário com todas as informações do caminho."""
#         return {
#             "nome": self.caminho.name,
#             **self.nomenclatura(self.caminho),
#             "validacoes": self.validar_caminho(self.caminho),
#             "estatisticas": self.obter_estatisticas(self.caminho),
#             "permissoes": self.verificar_permissoes(self.caminho),
#         }

#     def ler_arquivo_html(self, caminho_html: str) -> List[str]:
#         """Lê o conteúdo de um arquivo HTML e retorna uma lista de linhas do arquivo."""
#         try:
#             with open(caminho_html, "r", encoding="utf-8") as arquivo:
#                 return arquivo.readlines()
#         except (PermissionError, UnicodeDecodeError) as e:
#             raise RuntimeError(f"Erro ao ler o arquivo: {e}") from e

#     def process_html_file(
#         self, file_path: str
#     ) -> List[Dict[str, Union[str, Dict[str, Optional[str]]]]]:
#         """
#         Processa um arquivo HTML e retorna os dados das tags aceitas.

#         Args:
#             file_path (str): Caminho do arquivo HTML.

#         Returns:
#             List[Dict]: Lista de dicionários com os dados das tags.
#         """
#         lines = self.ler_arquivo_html(file_path)
#         all_tags_data = []

#         for line in lines:
#             html_tag = HtmlTag(tag_line=line)
#             html_tag.process_line()
#             all_tags_data.extend(html_tag.get_tags_data())

#         return all_tags_data

#     def gerar_json_completo(self) -> str:
#         """Gera um JSON completo com todas as informações do caminho e as tags HTML filtradas."""
#         informacoes = self.obter_informacoes()

#         # Só faz a leitura e processamento das tags HTML se for um arquivo
#         if self.validar_caminho(self.caminho)["eh_arquivo"]:
#             try:
#                 # conteudo_html = self.ler_arquivo_html(str(self.caminho))
#                 informacoes["tags_html"] = self.process_html_file(str(self.caminho))
#             except (ValueError, RuntimeError) as e:
#                 informacoes["erro"] = str(e)

#         return json.dumps(informacoes, indent=4, ensure_ascii=False)


# # # Exemplo de uso
# # if __name__ == "__main__":
# #     tipos_de_caminhos: Dict[str, str] = {
# #         "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html",
# #         # "Arquivo - Relativo e válido (genérico)": "../../Downloads/Chrome/copy-favoritos_23_12_2024.html",
# #     }
# #     for tipo, caminho_teste in tipos_de_caminhos.items():
# #         print(f"\nTipo do caminho: {tipo}")
# #         try:
# #             caminho_obj = InformacoesCaminho(caminho_string=caminho_teste)
# #             json_completo = caminho_obj.gerar_json_completo()
# #             print(json_completo)
# #         except FileNotFoundError as e:
# #             print(f"Erro: {e}")
# #         except (ValueError, RuntimeError) as e:
# #             print(f"Erro ao processar o caminho: {e}")
