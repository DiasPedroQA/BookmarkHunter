# pylint: disable=C, R, E, W

"""
Descrição:
    Este módulo define a classe PathModel para validação e manipulação de caminhos
    no sistema de arquivos. Ele utiliza métodos para obter informações detalhadas 
    como tipo, estatísticas, e resolução de links simbólicos e caminhos relativos.

Objetos:
    - PathModel: Representa e manipula um caminho no sistema operacional.

Dependências:
    Este módulo utiliza funções do arquivo 'services.py' para obter informações
    detalhadas sobre caminhos, como estatísticas e permissões.
"""

# import os
# import sys

# # Adiciona o diretório raiz do projeto ao sys.path
# dir_name = os.path.dirname(__file__)
# project_dir_name = os.path.join(dir_name, "../../")
# project_root = os.path.abspath(project_dir_name)
# sys.path.append(project_root)


# class PathModel:
#     """
#     Classe para validação e manipulação de caminhos do sistema de arquivos.
#     """

#     def __init__(self, caminho: str):
#         """
#         Inicializa o modelo com um caminho específico.

#         :param caminho: Caminho para validação e manipulação.
#         """
#         if not caminho or not isinstance(caminho, str):
#             raise ValueError("O caminho deve ser uma string não vazia.")
#         self.caminho_entrada: str = caminho

#     def tratar_link_simbolico(self, caminho_simbolico: str) -> str:
#         """
#         Resolve links simbólicos e retorna informações detalhadas.

#         :param path_obj: Objeto Path representando o link simbólico.
#         :return: Informações sobre o link simbólico em formato JSON.
#         """

#         path_obj: Path = Path(caminho_simbolico)
#         if not path_obj.is_symlink():
#             return self.gerar_resposta_json(
#                 mensagem=f"O caminho '{path_obj}' não é um link simbólico.",
#                 status="NOT_OK",
#             )

#         try:
#             caminho_resolvido: Path = path_obj.resolve(strict=True)
#             return self.gerar_resposta_json(
#                 mensagem="Link simbólico resolvido com sucesso.",
#                 caminho_original=self.caminho_entrada,
#                 caminho_resolvido=str(caminho_resolvido),
#                 tipo=self.determinar_tipo_caminho(caminho_resolvido),
#                 estatisticas=self.obter_estatisticas(caminho_resolvido),
#                 permissoes=obter_permissoes_caminho(caminho=caminho_resolvido),
#                 pasta_mae=self.obter_pasta_mae(caminho_resolvido),
#             )
#         except FileNotFoundError:
#             return self.gerar_resposta_json(
#                 mensagem=f"Link simbólico '{self.caminho_entrada}' inválido. Destino não encontrado.",
#                 status="NOT_OK",
#             )
#         except Exception as e:
#             return self.gerar_resposta_json(
#                 mensagem=f"Erro inesperado ao resolver link simbólico: {str(e)}",
#                 status="NOT_OK",
#             )

#     def tratar_caminho_existente(self, path_obj: Path) -> str:
#         """
#         Trata caminhos existentes e retorna informações detalhadas.

#         :param path_obj: Objeto Path representando o caminho.
#         :return: Informações sobre o caminho em formato JSON.
#         """
#         try:
#             # Verifica se o caminho é um arquivo ou diretório antes de prosseguir
#             tipo_caminho = self.determinar_tipo_caminho(path_obj)
#             estatisticas = self.obter_estatisticas(path_obj)
#             pasta_mae = self.obter_pasta_mae(path_obj)

#             return self.gerar_resposta_json(
#                 mensagem="Caminho válido.",
#                 caminho_original=self.caminho_entrada,
#                 caminho_resolvido=str(path_obj),
#                 tipo=tipo_caminho,
#                 estatisticas=estatisticas,
#                 pasta_mae=pasta_mae,
#             )
#         except Exception as e:
#             return self.gerar_resposta_json(
#                 mensagem=f"Erro ao tratar caminho existente: {str(e)}", status="NOT_OK"
#             )

#     def tratar_caminho_relativo(self, caminho_atual: str) -> str:
#         """
#         Resolve caminhos relativos para absolutos e valida sua existência.

#         :param caminho_atual: Caminho relativo a ser processado.
#         :return: Informações sobre o caminho em formato JSON.
#         """
#         if not isinstance(caminho_atual, str) or not caminho_atual.strip():
#             return self.gerar_resposta_json(
#                 mensagem="Caminho relativo inválido ou vazio.",
#                 caminho_original=caminho_atual,
#                 status="NOT_OK",
#             )

#         try:
#             caminho_resolvido = self.converter_para_absoluto(caminho_atual)
#             path_resolvido = Path(caminho_resolvido)

#             if path_resolvido.exists():
#                 return self.gerar_resposta_json(
#                     mensagem="Caminho relativo resolvido e válido.",
#                     caminho_original=self.caminho_entrada,
#                     caminho_resolvido=str(path_resolvido),
#                     tipo=self.determinar_tipo_caminho(path_resolvido),
#                     estatisticas=self.obter_estatisticas(path_resolvido),
#                     permissoes=obter_permissoes_caminho(caminho=path_resolvido),
#                     pasta_mae=self.obter_pasta_mae(path_resolvido),
#                 )

#             return self.gerar_resposta_json(
#                 mensagem=f"Caminho relativo '{self.caminho_entrada}' não existe.",
#                 caminho_original=self.caminho_entrada,
#                 status="NOT_OK",
#             )
#         except Exception as e:
#             return self.gerar_resposta_json(
#                 mensagem=f"Erro ao tratar caminho relativo: {str(e)}",
#                 caminho_original=self.caminho_entrada,
#                 status="NOT_OK",
#             )

#     def gerar_resposta_json(
#         self,
#         mensagem: str,
#         status: str = "ALL_OK",
#         **dados_caminho: Union[str, dict[str, Union[str, int]]],
#     ) -> str:
#         """
#         Gera uma resposta formatada em JSON.

#         :param mensagem: Mensagem descritiva do resultado.
#         :param status: Status do resultado (ALL_OK, NOT_OK, etc.).
#         :param dados_caminho: Dados adicionais a serem incluídos.
#         :return: Resposta formatada como JSON.
#         """
#         # Inicializa a estrutura básica de resposta
#         resposta: dict[str, str | dict[str, str | dict[str, str | int]]] = {
#             "mensagem": mensagem,
#             "status": status,
#             "dados_caminho": dados_caminho if dados_caminho else {},
#         }

#         # Gera um ID apenas se houver dados no campo "dados_caminho"
#         if dados_caminho:
#             resposta["dados_caminho"]["id_caminho"] = obter_id_unico(
#                 identificador=len(self.caminho_entrada)
#             )

#         try:
#             # Retorna a resposta formatada como JSON
#             return json.dumps(resposta, indent=4, ensure_ascii=False, sort_keys=True)
#         except Exception as e:
#             return json.dumps(
#                 {
#                     "mensagem": "Erro ao gerar resposta JSON.",
#                     "status": "NOT_OK",
#                     "dados_caminho": {},
#                 },
#                 indent=4,
#                 ensure_ascii=False,
#                 sort_keys=True,
#             )

#     def validar_caminho(self) -> str:
#         """
#         Valida o caminho e retorna informações formatadas como JSON.

#         :return: Informações detalhadas sobre o caminho em formato JSON.
#         """
#         if (
#             not isinstance(self.caminho_entrada, str)
#             or not self.caminho_entrada.strip()
#         ):
#             return self.gerar_resposta_json(
#                 mensagem="Caminho inválido ou vazio.", status="NOT_OK"
#             )

#         try:
#             path_obj = Path(self.caminho_entrada).resolve()

#             # Verifica se o caminho existe
#             if path_obj.exists():
#                 if path_obj.is_symlink():
#                     return self.tratar_link_simbolico(path_obj)
#                 return self.tratar_caminho_existente(path_obj)

#             # Verifica caminhos relativos
#             if (
#                 path_obj.is_relative_to(Path.cwd())
#                 or self.caminho_entrada.startswith("../")
#                 or self.caminho_entrada.startswith("/..")
#             ):
#                 return self.tratar_caminho_relativo(caminho_atual=self.caminho_entrada)

#             # Caminho inexistente
#             return self.gerar_resposta_json(
#                 mensagem=f"Caminho '{self.caminho_entrada}' não existe.",
#                 status="NOT_OK",
#             )
#         except Exception as e:
#             return self.gerar_resposta_json(
#                 mensagem=f"Erro ao validar caminho '{self.caminho_entrada}': {str(e)}",
#                 status="NOT_OK",
#             )

#     def obter_estatisticas(self, path_obj: Path) -> dict[str, Union[str, int]]:
#         """
#         Obtém estatísticas detalhadas sobre um caminho existente.

#         :param path_obj: Objeto Path do caminho.
#         :return: Dicionário com estatísticas do caminho.
#         """
#         if not path_obj.exists():
#             return {
#                 "data_acesso": "",
#                 "data_criacao": "",
#                 "data_modificacao": "",
#                 "tamanho": "",
#             }

#         try:
#             stats = path_obj.stat()
#             return {
#                 "data_acesso": obter_data_acesso(stats.st_atime),
#                 "data_criacao": obter_data_criacao(stats.st_ctime),
#                 "data_modificacao": obter_data_modificacao(stats.st_mtime),
#                 "tamanho": obter_tamanho_arquivo(stats.st_size),
#             }
#         except (FileNotFoundError, PermissionError) as e:
#             return {
#                 "data_acesso": "",
#                 "data_criacao": "",
#                 "data_modificacao": "",
#                 "tamanho": "",
#             }
#         except Exception as e:
#             return {
#                 "data_acesso": "",
#                 "data_criacao": "",
#                 "data_modificacao": "",
#                 "tamanho": "",
#             }

#     def converter_para_absoluto(self, caminho_relativo: str) -> str:
#         """
#         Converte um caminho relativo para um caminho absoluto.

#         :param caminho_relativo: Caminho relativo.
#         :return: Caminho absoluto como string.
#         """
#         if not isinstance(caminho_relativo, str) or not caminho_relativo.strip():
#             return ""

#         try:
#             # Remove o prefixo "/." caso exista
#             caminho_relativo = caminho_relativo.lstrip("/.")

#             # Converte para absoluto e resolve quaisquer componentes relativos
#             caminho_absoluto = str(
#                 (Path.home() / Path(caminho_relativo.lstrip("../"))).resolve()
#             )

#             return str(caminho_absoluto)

#         except Exception as e:
#             return ""

#     def determinar_tipo_caminho(self, path_obj: Path) -> str:
#         """
#         Determina o tipo de um caminho (Arquivo, Diretório ou Inválido).

#         :param path_obj: Objeto Path do caminho.
#         :return: Tipo do caminho como string.
#         """
#         if not isinstance(path_obj, Path):
#             return "Inválido"

#         if path_obj.exists():
#             if path_obj.is_file():
#                 return "Arquivo"
#             elif path_obj.is_dir():
#                 return "Diretório"
#             else:
#                 return "Outro Tipo"  # Para lidar com casos como dispositivos, links simbólicos, etc.
#         else:
#             return "Inválido"

#     def obter_pasta_mae(self, path_obj: Path) -> str:
#         """
#         Obtém o nome da pasta mãe de um caminho.

#         :param path_obj: Objeto Path do caminho.
#         :return: Nome da pasta mãe, ou uma string vazia se o caminho for inválido ou não tiver pasta mãe.
#         """
#         if not isinstance(path_obj, Path):
#             return ""

#         # Verifica se o caminho possui um diretório pai
#         if path_obj.parent == path_obj:
#             return ""

#         return path_obj.parent.name

import json
from pathlib import Path
import re


class CaminhoUtils:
    """Funções utilitárias para manipulação de caminhos."""

    @staticmethod
    def validar_caminho_como_string(caminho: str) -> bool:
        """Valida se o caminho é uma string relativa válida.

        Um caminho válido deve:
            - Começar com "./", "../", ou "/../".
            - Pode ser um nome de diretório ou arquivo que começa com ".".

        Args:
            caminho (str): O caminho a ser validado.

        Returns:
            bool: True se o caminho for uma string válida conforme as regras. False caso contrário.
        """
        if not isinstance(caminho, str) or not caminho.strip():
            return False

        # Regex para verificar os critérios
        padrao = r"^(?:\.{1,2}/|/\.{2}/|\.{1}[^/]*$)"
        return bool(re.match(padrao, caminho))

    @staticmethod
    def converter_para_absoluto(caminho: str) -> str:
        """Converte um caminho relativo para um caminho absoluto.

        Args:
            caminho (str): O caminho relativo a ser convertido.

        Returns:
            str: O caminho absoluto correspondente se válido, ou uma string vazia se inválido.

        Raises:
            ValueError: Se houver falha ao converter o caminho.
        """
        if not CaminhoUtils.validar_caminho_como_string(caminho):
            return caminho

        try:
            return str((Path.home() / Path(caminho.lstrip("./"))).resolve())
        except Exception as e:
            raise ValueError(
                f"Erro ao converter caminho '{caminho}' para absoluto: {e}"
            )

    @staticmethod
    def gerar_resposta_json(
        mensagem: str,
        status: str = "ALL_OK",
        **dados_caminho: dict[str, str]
    ) -> str:
        """Gera uma resposta formatada em JSON.

        Args:
            mensagem (str): Mensagem a ser incluída na resposta.
            status (str, optional): Status da operação. Padrão é "ALL_OK".
            **dados_caminho (Dict[str, Any]): Dados adicionais a serem incluídos na resposta.

        Returns:
            str: Uma string formatada em JSON com os dados fornecidos.

        Raises:
            ValueError: Se os argumentos `mensagem` ou `status` forem inválidos.
        """
        if not isinstance(mensagem, str) or not mensagem.strip():
            raise ValueError("A mensagem fornecida deve ser uma string não vazia.")

        if not isinstance(status, str):
            raise ValueError("O status deve ser uma string.")

        resposta: dict[str, str] = {
            "mensagem": mensagem,
            "status": status,
            "dados_caminho": dados_caminho,
        }
        return json.dumps(resposta, indent=4, ensure_ascii=False, sort_keys=True)


# # Testando os métodos com diferentes entradas
# caminhos = [
#     "./",
#     ".",
#     ".venv",
#     "../Downloads",
#     "../Downloads/",
#     "/../Downloads",
#     "/../Downloads/",
#     "/./",
#     "/../",
#     0,
#     -42,
#     123,
#     None,
#     [],
#     (),
#     {},
#     True,
#     False,
# ]

# # Garantir que 'caminhos' contém apenas strings
# caminhos_filtrados = [str(teste) for teste in caminhos if isinstance(teste, (str, int))]

# # Validação dos caminhos
# caminhos_validados: dict[str, bool] = {
#     teste: CaminhoUtils.validar_caminho_como_string(caminho=teste) for teste in caminhos_filtrados
# }

# # Filtrando os caminhos validados para manter apenas os que são True
# caminhos_validados_true: dict[str, bool] = {
#     chave: valor for chave, valor in caminhos_validados.items() if valor is True
# }

# # Conversão para caminhos absolutos
# caminhos_convertidos: dict[str, str] = {
#     teste: CaminhoUtils.converter_para_absoluto(caminho=teste) for teste in caminhos_filtrados
# }

# # Filtrando os caminhos convertidos para manter apenas os que não têm o mesmo valor que a chave
# caminhos_convertidos_diferentes: dict[str, str] = {
#     chave: valor for chave, valor in caminhos_convertidos.items() if chave != valor
# }

# # Gerar resposta em JSON com os dados filtrados
# resposta = CaminhoUtils.gerar_resposta_json(
#     mensagem="Teste de geração de resposta",
#     status="SUCCESS",
#     caminhos_validados=caminhos_validados_true,
#     caminhos_convertidos=caminhos_convertidos_diferentes,
# )

# print(resposta)




# # # Exemplo de conversão
# # try:
# #     caminho_absoluto = CaminhoUtils.converter_para_absoluto("../meu_caminho")
# #     print(caminho_absoluto)
# # except ValueError as e:
# #     print(e)

# # # Exemplo de resposta JSON
# # resposta = CaminhoUtils.gerar_resposta_json(
# #     mensagem="Caminho processado com sucesso",
# #     status="SUCCESS",
# #     caminho="algum/caminho"
# # )
# # print(resposta)


# # class CaminhoValidator:
# #     """Classe responsável por validar e categorizar caminhos."""

# #     @staticmethod
# #     def determinar_tipo(path_obj: Path) -> str:
# #         """Determina o tipo do caminho."""
# #         if not path_obj.exists():
# #             return "Inválido"
# #         if path_obj.is_file():
# #             return "Arquivo"
# #         if path_obj.is_dir():
# #             return "Diretório"
# #         return "Outro Tipo"

# #     @staticmethod
# #     def obter_estatisticas(path_obj: Path) -> dict[str, Union[str, int]]:
# #         """Obtém estatísticas do caminho."""
# #         try:
# #             stats = path_obj.stat()
# #             return {
# #                 "tamanho": stats.st_size,
# #                 "data_modificacao": stats.st_mtime,
# #                 "data_criacao": stats.st_ctime,
# #             }
# #         except Exception:
# #             return {}


# # class PathModel:
# #     """Classe principal para manipulação de caminhos."""

# #     def __init__(self, caminho: str):
# #         if not CaminhoUtils.validar_caminho_como_string(caminho):
# #             raise ValueError("O caminho deve ser uma string não vazia.")
# #         self.caminho_entrada = caminho

# #     def validar(self) -> str:
# #         """Valida e processa o caminho."""
# #         try:
# #             path_obj = Path(self.caminho_entrada)
# #             if not path_obj.exists():
# #                 return CaminhoUtils.gerar_resposta_json(
# #                     mensagem=f"Caminho '{path_obj}' não encontrado.", status="NOT_OK"
# #                 )
# #             return self._processar_caminho(path_obj)
# #         except Exception as e:
# #             return CaminhoUtils.gerar_resposta_json(
# #                 mensagem=f"Erro ao validar o caminho '{path_obj}': {e}", status="NOT_OK"
# #             )

# #     def _processar_caminho(self, path_obj: Path) -> str:
# #         """Processa o caminho após validação."""
# #         tipo = CaminhoValidator.determinar_tipo(path_obj)
# #         stats = CaminhoValidator.obter_estatisticas(path_obj)
# #         return CaminhoUtils.gerar_resposta_json(
# #             mensagem="Caminho processado com sucesso.",
# #             tipo=tipo,
# #             estatisticas=stats,
# #             caminho_resolvido=str(path_obj),
# #         )


# # # Exemplo de uso:
# # caminhos_para_validar: list[str] = [
# #     "/caminho/inexistente/",
# #     "../../Downloads/Chrome/favoritos.html",
# #     "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
# #     "/home/pedro-pm-dias/Downloads/Chrome/favoritos_link_simbólico",
# #     "/home/pedro-pm-dias/Downloads/Chrome/",
# #     "../../Downloads/Chrome",
# #     "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
# #     "../../Downloads/Chrome/favoritos_23_12_2024.html",
# #     "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
# #     "/../../Downloads/Chrome/Teste/",
# # ]

# # for caminho in caminhos_para_validar:
# #     modelo = PathModel(caminho)
# #     assert modelo.caminho_entrada == caminho
# #     validacao = json.loads(modelo.validar())
# #     print("\n\n", validacao)
