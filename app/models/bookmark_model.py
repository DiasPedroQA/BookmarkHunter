# app/models/bookmark_model.py

"""
Módulo para processar tags HTML e extrair informações relevantes.

Este módulo fornece classes para manipular documentos HTML, com foco em processar
tags específicas e transformar as informações extraídas em um formato estruturado
como JSON. Ele utiliza utilitários de conversão e geração de identificadores.

Classes:
    BaseTagModel: Classe base que fornece utilitários de conversão e geração.
    ObjetoTag: Especializada na extração e processamento de tags <h3> e <a>.

"""

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from typing import Any, Dict, List
from bs4 import BeautifulSoup, Tag
from app.utils import ConversoresUtils, GeradoresUtils


class BaseTagModel(ConversoresUtils, GeradoresUtils):
    """
    Classe para representar uma tag HTML com funcionalidades base.
    Herdando de BaseProcessor, possibilita o uso de utilitários para processar atributos.
    """

    def __init__(self):
        """
        Define os atributos da tag e inicializa utilitários de conversão e geração.
        """
        super().__init__()
        self.conversores = ConversoresUtils()
        self.geradores = GeradoresUtils()
        self._tag_id: str = ""
        self._tag_name: str = ""
        self._tag_text_content: str = ""
        self._tag_atributos: Dict[str, str] = {}

    @property
    def tag_id(self) -> str:
        """
        Retorna o ID da tag.
        """
        if self._tag_name == "" or self._tag_text_content == "":
            raise ValueError(
                "Todos os dados da tag precisam ser definidos antes de acessar o ID."
            )
        if not self._tag_id:
            self._tag_id = self.geradores.gerar_id()
        return self._tag_id

    @property
    def tag_name(self) -> str:
        """
        Retorna o nome da tag.
        """
        return self._tag_name

    @tag_name.setter
    def tag_name(self, value: str):
        """
        Define o nome da tag.
        """
        self._tag_name = value

    @property
    def tag_text_content(self) -> str:
        """
        Retorna o conteúdo de texto da tag.
        """
        return self._tag_text_content

    @tag_text_content.setter
    def tag_text_content(self, value: str):
        """
        Define o conteúdo de texto da tag.
        """
        self._tag_text_content = value

    @property
    def tag_atributos(self) -> Dict[str, str]:
        """
        Retorna os atributos da tag.
        """
        return self._tag_atributos

    @tag_atributos.setter
    def tag_atributos(self, value: Dict[str, str]):
        """
        Define os atributos da tag.
        """
        self._tag_atributos = value

    def dados_definidos(self) -> bool:
        """
        Verifica se os dados da tag foram definidos.
        """
        return bool(self._tag_name and self._tag_text_content and self._tag_atributos)

    def processar_atributos_com_timestamps(self):
        """
        Converte atributos que possuem timestamps para o formato de data e hora brasileiro.
        """
        for key, val in self._tag_atributos.items():
            if val.isdigit():
                self._tag_atributos[key] = self.converter_timestamp_para_data_hora_br(val)


class ObjetoTag(BaseTagModel):
    """
    Classe para processar e gerenciar tags HTML.
    """

    tags_validas: set[str] = {"title", "h3", "a"}
    atributos_validos: set[str] = {"href", "add_date", "last_modified"}

    def __init__(self, html_content: str):
        """
        Inicializa o objeto ObjetoTag.
        """
        super().__init__()
        self._tags_brutas = html_content
        self._tags_processadas: List[BaseTagModel] = []

    def _extrair_tags(self) -> List[Tag]:
        """
        Extrai as tags válidas do conteúdo HTML.
        """
        sopa = BeautifulSoup(self._tags_brutas, 'html.parser')
        return sopa.find_all(list(self.tags_validas))

    def _processar_atributos(self, obj_tag: Tag) -> Dict[str, str]:
        """
        Processa os atributos das tags, filtrando apenas os válidos.
        """
        return {key: obj_tag.attrs.get(key, "") for key in self.atributos_validos}

    def _criar_objeto_tag(self, obj_tag: Tag) -> BaseTagModel:
        """
        Cria um objeto BaseTagModel a partir de uma tag HTML extraída.
        """
        obj = BaseTagModel()
        obj.tag_name = obj_tag.name
        obj.tag_text_content = obj_tag.text.strip()
        obj.tag_atributos = self._processar_atributos(obj_tag)
        obj.processar_atributos_com_timestamps()  # Aplica a conversão
        return obj

    def raspar_e_processar_tags(self) -> List[Dict[str, Any]]:
        """
        Raspa as tags válidas e processa seus dados em um formato estruturado.
        """
        tags_extraidas = self._extrair_tags()
        for tag in tags_extraidas:
            objeto_tag = self._criar_objeto_tag(tag)
            if objeto_tag.dados_definidos():
                self._tags_processadas.append(objeto_tag)

        return [
            {
                "id": tag.tag_id,
                "name": tag.tag_name,
                "content": tag.tag_text_content,
                "attributes": {k: v for k, v in tag.tag_atributos.items() if v},
            }
            for tag in self._tags_processadas
        ]


# # Exemplo de uso
# string_html: str = """
#     <html>
#         <head>
#             <title ADD_DATE="16948752316">Teste da classe ObjetoTag</title>
#         </head>
#         <body>
#             <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#             <DL><p>
#             <DT><A HREF="https://dev.to/leandronsp/" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
#             <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
#             <DL><p>
#             <DT><A HREF="https://martinfowler.com/articles" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
#         </body>
#     </html>
# """
# objeto = ObjetoTag(string_html)
# raspagem = objeto.raspar_e_processar_tags()

# # Resultado final
# for tag_raspada in raspagem:
#     print(tag_raspada)
