# pylint: disable=E0611

"""
Descrição dos modelos de dados utilizados na aplicação.

Objetos:
    - FileModel: Representa e manipula um arquivo no sistema operacional.

Dependências:
    Este módulo utiliza funções do arquivo 'services.py' para obter informações
    detalhadas sobre arquivos, como tamanho e permissões.
"""

import logging
from typing import Union
from app.models.modelo_caminho import PathModel


class FileModel(PathModel):
    """
    Classe que representa e manipula um arquivo no sistema operacional.
    """

    def __init__(self, caminho_original: str):
        """
        Inicializa um objeto FileModel a partir de um caminho de arquivo.
        """
        super().__init__(caminho_original)

        if not self.caminho_existe:
            logging.warning("O arquivo '%s' não existe.", self.caminho_resolvido)

        if not self.is_arquivo:
            logging.warning(
                "O caminho '%s' não é um arquivo válido.", self.caminho_resolvido
            )


    def gerar_dados(self) -> dict[str, Union[str, int, bool]]:
        """
        Gera um dicionário com informações detalhadas sobre o arquivo.

        Returns:
            dict[str, Union[str, int, bool]]: Dados sobre o arquivo.
        """
        dados_arquivo = {
            "caminho_resolvido": self.caminho_resolvido,
            "caminho_existe": self.caminho_existe,
            "caminho_e_arquivo": self.is_arquivo,
        }

        return dados_arquivo


# # Exemplo de uso
# if __name__ == "__main__":
#     caminhos = [
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/",
#         "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#         "../../Downloads/Chrome/favoritos.html",
#         "/caminho/inexistente/",
#         "../../Downloads/Chrome/favoritos_23_12_2024.html",
#         "../../Downloads/Chrome/",
#         "../../Downloads/Chrome/Teste/",
#     ]

#     for caminho in caminhos:
#         file_obj = FileModel(caminho)
#         file_obj_json = file_obj.gerar_dados()
#         print('\n', file_obj_json, end="\n\n")
