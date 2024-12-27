# app/models/bookmark_model.py


"""
Módulo para processar tags HTML e extrair informações relevantes.

Este módulo fornece classes para manipular documentos HTML, com foco em processar
tags específicas e transformar as informações extraídas em um formato estruturado
como JSON. Ele utiliza utilitários de conversão e geração de identificadores.

Classes:
    BaseProcessor: Classe base que fornece utilitários de conversão e geração.
    ObjetoTag: Especializada na extração e processamento de tags <h3> e <a>.

"""

import os
import sys
import json
from typing import Dict, List, TypedDict, Optional
from bs4 import BeautifulSoup, Tag, ResultSet


# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.utils.conversores import ConversoresUtils
from app.utils.geradores import GeradoresUtils


class TagData(TypedDict):
    """Estrutura para representar dados de uma tag HTML."""

    object_tag_id: str
    object_tag_name: str
    object_text_content: str
    object_attributes: Dict[str, Optional[str]]


# Classe para configurar as tags
class TagConfig:
    """
    Configurações para o processamento de tags HTML.
    """

    TAGS_ALVO = ["a", "h3", "title"]  # Exemplo de tags HTML de interesse
    ATRIBUTOS_PERMITIDOS = {"href", "add_date", "last_modified"}

    def __str__(self) -> str:
        return f"TagConfig(TAGS_ALVO={self.TAGS_ALVO})"

class ObjetoTag:
    """Processa tags HTML para extrair informações estruturadas."""

    def __init__(
        self,
        html: str,
        conversores=ConversoresUtils(),
        geradores=GeradoresUtils(),
        config=TagConfig(),
    ):
        self.html = html
        self.conversores = conversores
        self.geradores = geradores
        self.config = config
        self.tags_ignoradas: List[str] = (
            []
        )  # Lista para armazenar nomes de tags ignoradas
        self.todas_tags: ResultSet[Tag] = (
            self._extrair_tags()
        )  # Armazenar todas as tags uma vez

    def _extrair_tags(self) -> ResultSet[Tag]:
        """Extrai todas as tags HTML do conteúdo."""
        soup = BeautifulSoup(self.html, "html.parser")
        return soup.find_all()  # Retorna todas as tags encontradas no HTML

    def _processar_atributos(self, tag: Tag) -> Dict[str, Optional[str]]:
        """Processa os atributos permitidos de uma tag HTML."""
        return {
            k.lower(): (
                self.conversores.converter_timestamp_para_data_br(tag_timestamp=v)
                if k.lower() in {"add_date", "last_modified"}
                else v
            )
            for k, v in tag.attrs.items()
            if k.lower() in self.config.ATRIBUTOS_PERMITIDOS
        }

    def _objeto_tag(self, tag: Tag) -> TagData:
        """Transforma uma tag HTML em um dicionário estruturado."""
        return TagData(
            object_tag_id=self.geradores.gerar_id(),
            object_tag_name=f"<{tag.name}>",
            object_text_content=tag.get_text(strip=True) or "",
            object_attributes=self._processar_atributos(tag),
        )

    def _validar_tag(self, tag: Tag) -> bool:
        """Valida se a tag está na lista de alvos."""
        return tag.name in self.config.TAGS_ALVO

    def processar_tags(self) -> str:
        """Processa todas as tags e retorna os dados válidos em formato JSON."""
        tags_validas = {}
        for indice_tag, tag in enumerate(self.todas_tags):
            if self._validar_tag(tag):
                tags_validas[f"tag_{indice_tag + 1}"] = self._objeto_tag(tag)
            else:
                self.tags_ignoradas.append(tag.name)
                # Apenas armazenar a tag ignorada, sem exibir ainda
        return json.dumps(tags_validas, indent=4, ensure_ascii=False)

    def resumo_processamento(self) -> Dict[str, int]:
        """Retorna um resumo do processamento com contagem de tags analisadas e ignoradas."""
        tags_total = len(self.todas_tags)
        tags_validadas = len(json.loads(self.processar_tags()))
        tags_ignoradas = tags_total - tags_validadas

        print("\nTags ignoradas:")
        if self.tags_ignoradas:
            # Exibe as tags ignoradas e quantas vezes ocorreram
            for tag_name in set(self.tags_ignoradas):
                print(
                    f"- <{tag_name}> ({self.tags_ignoradas.count(tag_name)}) ocorrências"
                )
        else:
            print("Nenhuma tag foi ignorada.")

        return {
            "total_tags_analisadas": tags_total,
            "total_tags_validas": tags_validadas,
            "total_tags_ignoradas": tags_ignoradas,
        }


# # Exemplo de uso com HTML de teste  # pylint: disable=C0301
# if __name__ == "__main__":
#     HTML_TESTE = """
#     <html>
#         <body>
#             <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#         <DL><p>
#             <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
#             <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
#         <DL><p>
#             <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
#         </body>
#     </html>
#     """

#     processador: ObjetoTag = ObjetoTag(html=HTML_TESTE)
#     json_tags: str = processador.processar_tags()
#     resumo = processador.resumo_processamento()

#     print("Tags Processadas:")
#     print(f"\n\njson_tags: {json_tags}")

#     print("\nResumo do Processamento:")
#     print(f"\n\nresumo: {resumo}")
