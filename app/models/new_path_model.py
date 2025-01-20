"""
Este módulo contém uma classe para análise e manipulação de strings relacionadas a caminhos de arquivos ou diretórios.

Funcionalidades principais:

1. Sanitização de caminhos: remove caracteres inválidos e verifica a validade do formato.
2. Extração de informações detalhadas, como:
   - Extensão do arquivo
   - Se o caminho é absoluto ou relativo
   - Número de diretórios
   - Raiz do caminho
   - Nome do arquivo (sem extensão)
   - Diretório principal
3. Fornecimento de dados estruturados através da classe `PathData`.
4. Tratamento robusto de erros para entradas inválidas.

Esta ferramenta é útil para pré-processar e validar caminhos
antes de manipulações mais complexas usando bibliotecas como `pathlib`.
"""

import re
from dataclasses import dataclass


@dataclass
class PathData:
    """
    Representa os dados de um caminho após análise e sanitização.
    """

    caminho_original: str
    caminho_sanitizado: str
    formato_valido: bool
    extensao_arquivo: str = ""  # Extensão do arquivo (se extraída)
    eh_absoluto: bool = False  # Indica se o caminho é absoluto
    numero_diretorios: int = 0  # Número de diretórios no caminho
    nome_arquivo: str = ""  # Nome do arquivo (sem extensão)
    pasta_principal: str = ""  # Diretório principal
    eh_relativo: bool = False  # Indica se o caminho é relativo


class AnalisadorCaminhoString:
    """
    Classe para análise e manipulação de strings relacionadas a caminhos.
    """

    def _formato_caminho_valido(self, caminho: str) -> bool:
        """
        Verifica se o formato do caminho é válido.

        Args:
            caminho (str): Caminho sanitizado para validação.

        Returns:
            bool: True se o formato for válido, False caso contrário.
        """
        if len(caminho) > 260:
            raise ValueError(
                f"O caminho '{caminho}' excede o limite de comprimento permitido."
            )

        return bool(re.match(r"^[a-zA-Z0-9_\-/\\.]+$", caminho))

    def _extrair_extensao_arquivo(self, caminho: str) -> str | None:
        """
        Extrai a extensão do arquivo do caminho, se existir.

        Args:
            caminho (str): Caminho para análise.

        Returns:
            str: Extensão do arquivo (com ponto), ou string vazia se não houver.
        """
        match = re.search(r"\.([a-zA-Z0-9]+)$", caminho)
        return f".{match.group(1)}" if match else None

    def _eh_caminho_absoluto(self, caminho: str) -> bool:
        """
        Verifica se o caminho é absoluto.

        Args:
            caminho (str): Caminho para análise.

        Returns:
            bool: True se o caminho for absoluto, False caso contrário.
        """
        return bool(re.match(r"^(?:[a-zA-Z]:\\|/home/[a-zA-Z0-9_-]+/)", caminho))

    def _contar_diretorios(self, caminho: str) -> int:
        """
        Conta o número de diretórios no caminho.

        Args:
            caminho (str): Caminho para análise.

        Returns:
            int: Número de diretórios no caminho.
        """
        caminho_normalizado = re.sub(
            r"\\+", "/", caminho
        )  # Normaliza separadores de diretórios
        diretorios = caminho_normalizado.split("/")[:-1]  # Ignora o arquivo no final
        return len([d for d in diretorios if d])

    def _extrair_nome_arquivo(self, caminho: str) -> str | None:
        """
        Extrai o nome do arquivo (sem extensão) do caminho.

        Args:
            caminho (str): Caminho para análise.

        Returns:
            str: O nome do arquivo, ou string vazia se não houver arquivo.
        """
        match = re.search(r"([^/\\]+)(?=\.[a-zA-Z0-9]+$)", caminho)
        return match.group(1) if match else None

    def _extrair_pasta_principal(self, caminho: str) -> str | None:
        """
        Extrai o diretório principal do caminho.

        Args:
            caminho (str): Caminho para análise.

        Returns:
            str: O nome do diretório principal, ou string vazia se não aplicável.
        """
        match = re.search(r"([^/\\]+)/[^/\\]+/?$", caminho)
        return match.group(1) if match else None

    def _eh_caminho_relativo(self, caminho: str) -> bool:
        """
        Verifica se o caminho é relativo.

        Args:
            caminho (str): Caminho para análise.

        Returns:
            bool: True se o caminho for relativo, False caso contrário.
        """
        return bool(re.match(r"^(?:\.{1,2})\/", caminho))

    def sanitizar_caminho(self, caminho: str) -> PathData:
        """
        Remove caracteres inválidos e sanitiza o caminho.

        Args:
            caminho (str): Caminho bruto fornecido pelo usuário.

        Returns:
            PathData: Objeto contendo o caminho original, sanitizado e validade do formato.
        """
        if not caminho:
            raise ValueError("O caminho fornecido é nulo ou vazio.")

        # Sanitização do caminho
        caminho_sanitizado: str = re.sub(r"[^a-zA-Z0-9\- _./\\:]", "", caminho)

        # Validar o formato do caminho
        formato_valido: bool = self._formato_caminho_valido(caminho_sanitizado)

        # Extração das informações
        extensao_arquivo: str | None = self._extrair_extensao_arquivo(
            caminho_sanitizado
        )
        eh_absoluto: bool = self._eh_caminho_absoluto(caminho_sanitizado)
        numero_diretorios: int = self._contar_diretorios(caminho_sanitizado)
        nome_arquivo: str | None = self._extrair_nome_arquivo(caminho_sanitizado)
        pasta_principal: str | None = self._extrair_pasta_principal(caminho_sanitizado)
        eh_relativo: bool = self._eh_caminho_relativo(caminho_sanitizado)

        return PathData(
            caminho_original=caminho,
            caminho_sanitizado=caminho_sanitizado,
            formato_valido=formato_valido,
            extensao_arquivo=extensao_arquivo,
            eh_absoluto=eh_absoluto,
            numero_diretorios=numero_diretorios,
            nome_arquivo=nome_arquivo,
            pasta_principal=pasta_principal,
            eh_relativo=eh_relativo,
        )


# Exemplo de uso
if __name__ == "__main__":
    caminhos_para_validar: list[str] = [
        "/caminho/inexistente/",
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
        "/home/pedro-pm-dias/Downloads/Chrome/",
        "../../Downloads/Chrome/favoritos.html",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "~/Downloads/Documentos/arquivo.txt",
        "//server/share/arquivos/relatório.xlsx",
        "/home/usuario/Meu Documento/arquivo.docx",
        "C:\\Program Files\\Aplicativos\\software.exe",
    ]

    for caminho_bruto in caminhos_para_validar:
        try:
            analisador = AnalisadorCaminhoString()
            dados_caminho = analisador.sanitizar_caminho(caminho_bruto)

            print(f"\n\nCaminho Original: {dados_caminho.caminho_original}")
            print(f"    Caminho Sanitizado: {dados_caminho.caminho_sanitizado}")
            print(f"    Formato Válido: {dados_caminho.formato_valido}")
            print(f"    Extensão do Arquivo: {dados_caminho.extensao_arquivo}")
            print(f"    Caminho Absoluto: {dados_caminho.eh_absoluto}")
            print(f"    Número de Diretórios: {dados_caminho.numero_diretorios}")
            print(f"    Nome do Arquivo: {dados_caminho.nome_arquivo}")
            print(f"    Pasta Principal: {dados_caminho.pasta_principal}")
            print(f"    Caminho Relativo: {dados_caminho.eh_relativo}")
        except ValueError as e:
            print(f"\n\nErro: {e}")
