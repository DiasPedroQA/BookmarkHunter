# pylint: disable=C, R, E, W

import re
from pathlib import Path

class AnalisadorCaminho:
    """
    Classe para analisar caminhos de arquivos e pastas no sistema operacional Ubuntu.
    Trabalha com strings e utiliza regex como auxiliar para validações.
    """

    def __init__(self, caminho):
        """
        Inicializa o analisador com um caminho fornecido.

        :param caminho: Caminho do arquivo ou pasta como string.
        """
        self.caminho = caminho

    def caminho_eh_absoluto(self):
        """
        Verifica se o caminho é absoluto com base em regras simples.

        :return: True se começar com '/', False caso contrário.
        """
        return self.caminho.startswith("/")

    def caminho_eh_relativo(self):
        """
        Verifica se o caminho é relativo (não absoluto).

        :return: True se o caminho for relativo, False caso contrário.
        """
        return not self.caminho_eh_absoluto()

    def caminho_eh_caminho_valido(self):
        """
        Verifica se o caminho contém apenas caracteres válidos.

        :return: True se o caminho for válido, False caso contrário.
        """
        padrao = r"^[\w\-./]+$"
        return bool(re.match(padrao, self.caminho))

    def caminho_obter_nome_arquivo(self):
        """
        Retorna o nome do arquivo ou pasta no final do caminho.

        :return: O nome do arquivo ou pasta.
        """
        partes = self.caminho.rstrip("/").split("/")
        return partes[-1] if partes else ""

    def caminho_obter_diretorio(self):
        """
        Retorna o diretório pai do caminho fornecido.

        :return: O diretório pai.
        """
        if "/" not in self.caminho.rstrip("/"):
            return ""
        return "/".join(self.caminho.rstrip("/").split("/")[:-1])

    def caminho_possui_extensao(self, extensao):
        """
        Verifica se o caminho possui uma extensão específica.

        :param extensao: Extensão do arquivo (e.g., '.html').
        :return: True se o arquivo tiver a extensão, False caso contrário.
        """
        return self.caminho.endswith(extensao)

    def caminho_contar_segmentos(self):
        """
        Conta quantos segmentos existem no caminho.

        :return: Número de segmentos no caminho.
        """
        return len([segmento for segmento in self.caminho.strip("/").split("/") if segmento])

    def caminho_converter_para_relativo(self, diretorio_referencia):
        """
        Converte o caminho absoluto para relativo, baseado em um diretório de referência.

        :param diretorio_referencia: Caminho absoluto para ser usado como referência.
        :return: Caminho relativo.
        """
        if self.caminho_eh_absoluto():
            return Path(self.caminho).relative_to(diretorio_referencia)
        return self.caminho

    def caminho_converter_para_absoluto(self, diretorio_referencia):
        """
        Converte um caminho relativo para absoluto, baseado em um diretório de referência.

        :param diretorio_referencia: Caminho absoluto para ser usado como referência.
        :return: Caminho absoluto.
        """
        if self.caminho_eh_relativo():
            return str(Path(diretorio_referencia) / self.caminho)
        return self.caminho


class AnalisadorPathlib(AnalisadorCaminho):
    """
    Classe para análise de caminhos de arquivos e pastas utilizando pathlib.
    Herda funcionalidades de AnalisadorCaminho e expande com recursos adicionais.
    """

    def __init__(self, caminho):
        """
        Inicializa o analisador com um caminho fornecido.

        :param caminho: Caminho do arquivo ou pasta como string ou objeto Path.
        """
        super().__init__(caminho)  # Inicializa AnalisadorCaminho
        self.caminho_pathlib = Path(caminho)

    def pathlib_eh_arquivo(self):
        """
        Verifica se o caminho é um arquivo.

        :return: True se for um arquivo, False caso contrário.
        """
        return self.caminho_pathlib.is_file()

    def pathlib_eh_diretorio(self):
        """
        Verifica se o caminho é um diretório.

        :return: True se for um diretório, False caso contrário.
        """
        return self.caminho_pathlib.is_dir()

    def pathlib_obter_nome(self):
        """
        Retorna o nome do arquivo ou diretório.

        :return: Nome do arquivo ou diretório como string.
        """
        return self.caminho_pathlib.name

    def pathlib_obter_nome_sem_extensao(self):
        """
        Retorna o nome do arquivo sem a extensão.

        :return: Nome do arquivo sem extensão.
        """
        return self.caminho_pathlib.stem

    def pathlib_obter_extensao(self):
        """
        Retorna a extensão do arquivo.

        :return: Extensão do arquivo como string.
        """
        return self.caminho_pathlib.suffix

    def pathlib_obter_pai(self):
        """
        Retorna o diretório pai do caminho.

        :return: Diretório pai como objeto Path.
        """
        return self.caminho_pathlib.parent

    def pathlib_existe(self):
        """
        Verifica se o caminho existe.

        :return: True se existir, False caso contrário.
        """
        return self.caminho_pathlib.exists()

    def pathlib_eh_absoluto(self):
        """
        Verifica se o caminho é absoluto.

        :return: True se for absoluto, False caso contrário.
        """
        return self.caminho_pathlib.is_absolute()

    def pathlib_obter_metadados(self):
        """
        Obtém metadados detalhados do caminho.

        :return: Dicionário com informações detalhadas.
        """
        estatisticas = self.caminho_pathlib.stat()
        return {
            "tamanho_bytes": estatisticas.st_size,
            "criado": estatisticas.st_ctime,
            "modificado": estatisticas.st_mtime,
            "ultimo_acesso": estatisticas.st_atime,
            "permissoes": estatisticas.st_mode,
            "dispositivo": estatisticas.st_dev,
            "inode": estatisticas.st_ino,
            "links": estatisticas.st_nlink,
            "id_usuario": estatisticas.st_uid,
            "id_grupo": estatisticas.st_gid,
            "eh_link_simbolico": self.caminho_pathlib.is_symlink(),
            "eh_ponto_montagem": self.caminho_pathlib.is_mount(),
            "existe": self.caminho_pathlib.exists(),
        }

    def pathlib_resolver_caminho(self):
        """
        Retorna o caminho absoluto e resolvido (sem "." ou "..").

        :return: Caminho absoluto resolvido como objeto Path.
        """
        return self.caminho_pathlib.resolve()

    def pathlib_contar_segmentos(self):
        """
        Conta o número de segmentos no caminho.

        :return: Número de segmentos como inteiro.
        """
        return len(self.caminho_pathlib.parts)

    def obter_informacoes_combinadas(self):
        """
        Obtém um dicionário contendo todas as informações detalhadas.

        :return: Dicionário com informações do caminho.
        """
        return {
            "eh_absoluto": self.pathlib_eh_absoluto(),
            "eh_valido": self.caminho_eh_caminho_valido(),
            "nome_arquivo": self.caminho_obter_nome_arquivo(),
            "diretorio": self.caminho_obter_diretorio(),
            "possui_extensao": self.caminho_possui_extensao(self.pathlib_obter_extensao()),
            "contagem_segmentos": self.caminho_contar_segmentos(),
            "eh_arquivo": self.pathlib_eh_arquivo(),
            "eh_diretorio": self.pathlib_eh_diretorio(),
            "nome": self.pathlib_obter_nome(),
            "nome_sem_extensao": self.pathlib_obter_nome_sem_extensao(),
            "extensao": self.pathlib_obter_extensao(),
            "pai": str(self.pathlib_obter_pai()),
            "metadados": self.pathlib_obter_metadados(),
            "caminho_resolvido": str(self.pathlib_resolver_caminho()),
        }

    def pathlib_converter_para_relativo(self, diretorio_referencia):
        """
        Converte o caminho absoluto para relativo, baseado em um diretório de referência.

        :param diretorio_referencia: Caminho absoluto para ser usado como referência.
        :return: Caminho relativo.
        """
        if self.pathlib_eh_absoluto():
            return self.caminho_pathlib.relative_to(diretorio_referencia)
        return self.caminho_pathlib

    def pathlib_converter_para_absoluto(self, diretorio_referencia):
        """
        Converte um caminho relativo para absoluto, baseado em um diretório de referência.

        :param diretorio_referencia: Caminho absoluto para ser usado como referência.
        :return: Caminho absoluto.
        """
        if self.pathlib_eh_relativo():
            return self.caminho_pathlib.resolve()
        return self.caminho_pathlib


if __name__ == "__main__":
    # Caminho para análise
    caminhos_para_ler = [
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "../../Downloads/Chrome/",
    ]
    
    for caminho in caminhos_para_ler:
        # Inicializar o objeto AnalisadorPathlib
        analisador = AnalisadorPathlib(caminho)
        
        # Obter as informações detalhadas individualmente
        informacoes = analisador.obter_informacoes_combinadas()
        
        print('_' * 50)
        for chave, valor in informacoes.items():
            if isinstance(valor, dict):
                for chaveIN, valorIN in valor.items():
                    print(f"{chaveIN}: {valorIN}")
            print(f"{chave}: {valor}")
        print('_' * 50)
