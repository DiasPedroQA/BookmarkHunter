# app/models/bookmark_model.py

"""
Este módulo contém a definição da classe `Marcador`, que representa um marcador
de URL. A classe inclui atributos como título, href (URL), data de adição, 
última modificação e uma associação opcional com um arquivo.

A classe oferece suporte para a criação e manipulação de marcadores, com a
possibilidade de incluir metadados como datas e arquivos associados.

Classes:
    - Marcador: Representa um marcador de URL com atributos e suporte para 
      associação a arquivos.
"""

import json
from typing import Optional
from app.models.file_model import File


class Marcador:
    """
    Representa um marcador de URL com atributos básicos e suporte para associação a arquivos.

    Atributos:
        titulo (str): O título do marcador.
        href (str, opcional): O endereço URL do marcador.
        data_adicao (str, opcional): A data em que o marcador foi adicionado, em formato de string.
        ultima_modificacao (str, opcional): A data de modificação do marcador, em formato de string.
        arquivo (File, opcional): A referência ao arquivo associado ao marcador.
    """

    def __init__(
        self,
        titulo: str,
        href: Optional[str] = None,
        data_adicao: Optional[str] = None,
        ultima_modificacao: Optional[str] = None,
        arquivo: Optional["File"] = None,
    ):
        """
        Inicializa um objeto Marcador.

        Args:
            titulo (str): O título do marcador.
            href (str, opcional): O endereço URL do marcador. Padrão é None.
            data_adicao (str, opcional): A data de adição do marcador, em formato de string. Padrão é None.
            ultima_modificacao (str, opcional): A data da última modificação do marcador, em formato de string. Padrão é None.
            arquivo (File, opcional): O arquivo associado ao marcador. Padrão é None.
        """
        self.titulo = titulo
        self.href = href
        self.data_adicao = data_adicao
        self.ultima_modificacao = ultima_modificacao
        self.arquivo = arquivo  # Relacionamento com o objeto Arquivo

    def __repr__(self) -> str:
        """
        Retorna uma representação em string do objeto Marcador.

        Returns:
            str: Representação do objeto Marcador.
        """
        return (
            f"<Marcador(titulo={self.titulo}, href={self.href}, "
            f"data_adicao={self.data_adicao}, ultima_modificacao={self.ultima_modificacao})>"
        )

    def para_json(self) -> str:
        """
        Retorna todos os dados do objeto em formato JSON.

        Returns:
            str: Uma string JSON com os dados do objeto.
        """
        dados = {
            "titulo": self.titulo,
            "href": self.href,
            "data_adicao": self.data_adicao,
            "ultima_modificacao": self.ultima_modificacao,
            "arquivo": (
                self.arquivo.nome if self.arquivo and hasattr(self.arquivo, 'nome') else None
            ),  # Verifica se o arquivo tem o atributo 'nome'
        }
        return json.dumps(dados, indent=4)
