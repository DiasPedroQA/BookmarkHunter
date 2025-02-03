# # app/models/favorite_model.py
# # pylint: disable=C, R, E, W


# """
# Este módulo define a classe `HtmlTag`, que representa uma tag HTML com seus atributos e conteúdo.

# A classe oferece métodos para:
# - Processar e converter os atributos das tags,
# incluindo a conversão de timestamps para um formato de data e hora brasileiro.
# - Serializar as tags em formato de dicionário e JSON,
# excluindo atributos específicos (como 'ICON').
# - Manipular tags HTML específicas, como `<h3>` e `<a>`,
# com a extração e formatação adequada de seus atributos e conteúdo.

# Funções principais:
# - `convert_timestamp`: Converte um timestamp em segundos para o formato de data e hora brasileiro.
# - `process_attributes`: Processa os atributos de uma tag, realizando a conversão de timestamps e filtragem.
# - `para_dict`: Converte uma instância de `HtmlTag` em um dicionário, pronto para serialização em JSON.
# - `para_json`: Serializa a tag para uma string JSON formatada.

# Exemplo de uso:
#     html_tag = HtmlTag("a", {"href": "https://example.com", "add_date": "1609459200"}, "Example Link")
#     print(html_tag.para_json())

# Este módulo é útil para aplicações que necessitam processar e
# manipular dados de tags HTML em formatos estruturados como JSON.
# """


# import json
# import sys
# from pathlib import Path
# from typing import Dict, List, Optional, Union
# from bs4 import BeautifulSoup, Tag

# # Obtém o diretório raiz do projeto
# project_root = Path(__file__).resolve().parent.parent
# sys.path.append(str(project_root))

# from app.services.global_services import GeneralServices


# class HtmlTag:
#     """
#     A classe `HtmlTag` processa tags HTML específicas, como `<h3>` e `<a>`,
#     extraindo e formatando seus atributos e conteúdo.

#     Atributos:
#         ACCEPTED_TAGS (List[str]): Lista de tags HTML aceitas para processamento.
#         line_content (str): Conteúdo da linha HTML a ser processada.
#         timestamp_converter (GeneralServices): Instância do serviço para conversão de timestamps.
#         tags_data (List[Dict]): Lista de tags processadas e seus atributos.
#     """

#     ACCEPTED_TAGS = ["h3", "a"]

#     def __init__(self, tag_line: Optional[str] = None) -> None:
#         """
#         Inicializa a instância da classe HtmlTag.

#         Args:
#             tag_line (Optional[str]): Linha de conteúdo HTML a ser processada.
#         """
#         self.line_content = tag_line
#         self.timestamp_converter = GeneralServices()
#         self.tags_data: List[Dict[str, Union[str, Dict[str, Union[str, None]]]]] = []

#     def process_line(self) -> None:
#         """
#         Processa a linha de HTML para extrair tags aceitas e seus atributos.
#         """
#         if not self.line_content:
#             return

#         soup = BeautifulSoup(self.line_content, "html.parser")
#         for element in soup.descendants:
#             if isinstance(element, Tag) and element.name in self.ACCEPTED_TAGS:
#                 self.tags_data.append(self._extract_tag_data(element))

#     def _extract_tag_data(
#         self, element: Tag
#     ) -> Dict[str, Union[str, Dict[str, Union[str, None]]]]:
#         """
#         Extrai os dados de uma tag específica.

#         Args:
#             element (Tag): Elemento HTML a ser processado.

#         Returns:
#             Dict[str, Union[str, Dict[str, Union[str, None]]]]: Dicionário com os dados da tag.
#         """
#         tag_data = {
#             "tag": element.name,
#             "attributes": {
#                 "text_content": element.get_text(strip=True),
#                 "add_date": self.timestamp_converter.converter_timestamp(
#                     element.get("add_date", "")
#                 ),
#             },
#         }

#         if element.name == "a":
#             tag_data["attributes"]["href"] = element.get("href", "")
#         elif element.name == "h3":
#             tag_data["attributes"]["last_modified"] = (
#                 self.timestamp_converter.converter_timestamp(
#                     element.get("last_modified", "")
#                 )
#             )
#             tag_data["attributes"]["personal_toolbar_folder"] = element.get(
#                 "personal_toolbar_folder", ""
#             )

#         return tag_data

#     def get_tags_data(self) -> List[Dict[str, Union[str, Dict[str, Union[str, None]]]]]:
#         """
#         Retorna os dados das tags processadas.

#         Returns:
#             List[Dict]: Lista de dicionários com os dados das tags.
#         """
#         return self.tags_data

#     def to_dict(self) -> List[Dict[str, Union[str, Dict[str, Union[str, None]]]]]:
#         """
#         Converte os dados das tags em um formato de dicionário.

#         Returns:
#             List[Dict]: Lista de dicionários com os dados das tags.
#         """
#         return self.get_tags_data()

#     def to_json(self) -> str:
#         """
#         Serializa os dados das tags em uma string JSON formatada.

#         Returns:
#             str: String JSON formatada.
#         """
#         return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)


# # def read_html_file(file_path: str) -> List[str]:
# #     """
# #     Lê um arquivo HTML e retorna uma lista de linhas.

# #     Args:
# #         file_path (str): Caminho do arquivo HTML.

# #     Returns:
# #         List[str]: Lista de linhas do arquivo.
# #     """
# #     try:
# #         with open(file_path, "r", encoding="utf-8") as file:
# #             return file.readlines()
# #     except (PermissionError, UnicodeDecodeError) as e:
# #         raise RuntimeError(f"Erro ao ler o arquivo: {e}") from e


# # def process_html_file(
# #     file_path: str,
# # ) -> List[Dict[str, Union[str, Dict[str, Union[str, None]]]]]:
# #     """
# #     Processa um arquivo HTML e retorna os dados das tags aceitas.

# #     Args:
# #         file_path (str): Caminho do arquivo HTML.

# #     Returns:
# #         List[Dict]: Lista de dicionários com os dados das tags.
# #     """
# #     lines = read_html_file(file_path)
# #     all_tags_data = []

# #     for line in lines:
# #         html_tag = HtmlTag(tag_line=line)
# #         html_tag.process_line()
# #         all_tags_data.extend(html_tag.get_tags_data())
# #     return all_tags_data


# # # Exemplo de uso
# # if __name__ == "__main__":
# #     html_file_path = (
# #         "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html"
# #     )

# #     # Processa o arquivo HTML e obtém os dados das tags
# #     tags_data = process_html_file(html_file_path)

# #     # Exibe o resultado em formato JSON
# #     print(json.dumps(tags_data, indent=4, ensure_ascii=False))
