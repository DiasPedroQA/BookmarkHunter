# pylint: disable=C, R, E, W

import re
from pathlib import Path
from typing import Dict, Union


class AnalisadorCaminhoIntegrado:
    """
    Classe para analisar e manipular caminhos de arquivos e diretórios.

    Atributos:
        caminho (str): O caminho inicial fornecido.
        diretorio_referencia (str): O diretório de referência para caminhos relativos.
        caminho_pathlib (Path): Objeto Path do módulo pathlib para manipulação de caminhos.

    Métodos:
        __init__(caminho_inicial: str, referencia_dir: str = "") -> None:
            Inicializa a classe com o caminho inicial e o diretório de referência.

        eh_absoluto() -> bool:
            Verifica se o caminho é absoluto.

        eh_relativo() -> bool:
            Verifica se o caminho é relativo.

        eh_valido() -> bool:
            Verifica se o caminho é válido com base em um padrão regex.

        obter_nome() -> str:
            Obtém o nome do arquivo ou diretório do caminho.

        obter_nome_sem_extensao() -> str:
            Obtém o nome do arquivo sem a extensão.

        obter_extensao() -> str:
            Obtém a extensão do arquivo.

        obter_diretorio_pai() -> str:
            Obtém o diretório pai do caminho.

        possui_extensao(extensao: str) -> bool:
            Verifica se o caminho possui a extensão fornecida.

        contar_segmentos() -> int:
            Conta o número de segmentos no caminho.

        obter_metadados() -> Dict[str, Union[int, float]]:
            Obtém os metadados do caminho se ele existir.

        resolver_caminho() -> str:
            Resolve o caminho absoluto do caminho fornecido.

        converter_para_relativo() -> str:
            Converte o caminho para um caminho relativo com base no diretório de referência.

        converter_para_absoluto() -> str:
            Converte o caminho para um caminho absoluto com base no diretório de referência.

        obter_informacoes_combinadas() -> dict:
            Obtém várias informações combinadas sobre o caminho, incluindo metadados, se disponíveis.
    """

    def __init__(self, caminho_inicial: str, referencia_dir: str = "") -> None:
        self.caminho: str = caminho_inicial
        self.diretorio_referencia: str = referencia_dir
        self.caminho_pathlib = Path(caminho)

    def eh_absoluto(self) -> bool:
        try:
            return self.caminho_pathlib.is_absolute()
        except AttributeError as e:
            print(f"Erro ao verificar se é absoluto: {e}")
            return False

    def eh_relativo(self) -> bool:
        try:
            return not self.eh_absoluto()
        except AttributeError as e:
            print(f"Erro ao verificar se é relativo: {e}")
            return False

    def eh_valido(self) -> bool:
        try:
            padrao = r"^[\w\-./]+$"
            return bool(re.match(padrao, self.caminho))
        except re.error as e:
            print(f"Erro ao validar caminho: {e}")
            return False

    def obter_nome(self) -> str:
        try:
            return self.caminho_pathlib.name
        except AttributeError as e:
            print(f"Erro ao obter nome: {e}")
            return ""

    def obter_nome_sem_extensao(self) -> str:
        try:
            return self.caminho_pathlib.stem
        except AttributeError as e:
            print(f"Erro ao obter nome sem extensão: {e}")
            return ""

    def obter_extensao(self) -> str:
        try:
            return self.caminho_pathlib.suffix
        except AttributeError as e:
            print(f"Erro ao obter extensão: {e}")
            return ""

    def obter_diretorio_pai(self) -> str:
        try:
            return str(self.caminho_pathlib.parent)
        except AttributeError as e:
            print(f"Erro ao obter diretório pai: {e}")
            return ""

    def possui_extensao(self, extensao: str) -> bool:
        try:
            return self.caminho.endswith(extensao)
        except AttributeError as e:
            print(f"Erro ao verificar extensão: {e}")
            return False

    def contar_segmentos(self) -> int:
        try:
            return len(self.caminho_pathlib.parts)
        except AttributeError as e:
            print(f"Erro ao contar segmentos: {e}")
            return 0

    def obter_metadados(self) -> Dict[str, Union[int, float]]:
        try:
            if self.caminho_pathlib.exists():
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
            else:
                return {}
        except OSError as e:
            print(f"Erro ao obter metadados: {e}")
            return {}

    def resolver_caminho(self) -> str:
        try:
            return str(self.caminho_pathlib.resolve())
        except OSError as e:
            print(f"Erro ao resolver caminho: {e}")
            return ""

    def converter_para_relativo(self) -> str:
        try:
            if self.eh_absoluto():
                return str(self.caminho_pathlib.relative_to(self.diretorio_referencia))
            return str(self.caminho_pathlib)
        except ValueError as e:
            print(f"Erro ao converter para caminho relativo: {e}")
            return ""

    def converter_para_absoluto(self) -> str:
        try:
            if self.eh_relativo():
                return str(
                    (Path(self.diretorio_referencia) / self.caminho_pathlib).resolve()
                )
            return str(self.caminho_pathlib)
        except ValueError as e:
            print(f"Erro ao converter para caminho absoluto: {e}")
            return ""

    def obter_informacoes_combinadas(self) -> dict:
        try:
            info_combinadas = {
                "eh_absoluto": self.eh_absoluto(),
                "eh_valido": self.eh_valido(),
                "nome_caminho": self.obter_nome(),
                "diretorio_pai": self.obter_diretorio_pai(),
                "extensao": self.obter_extensao(),
                "possui_extensao": self.possui_extensao(self.obter_extensao()),
                "contagem_segmentos": self.contar_segmentos(),
                "eh_arquivo": self.caminho_pathlib.is_file(),
                "eh_diretorio": self.caminho_pathlib.is_dir(),
                "nome_sem_extensao": self.obter_nome_sem_extensao(),
            }

            # Tentar usar caminho absoluto se o caminho não for encontrado
            if (
                not self.caminho_pathlib.exists()
                and self.eh_relativo()
                and self.eh_valido()
            ):
                caminho_absoluto = self.converter_para_absoluto()
                if Path(caminho_absoluto).exists():
                    self.caminho_pathlib = Path(caminho_absoluto)
                    info_combinadas["metadados"] = self.obter_metadados()
                else:
                    info_combinadas["erro"] = (
                        "O caminho absoluto montado não foi encontrado."
                    )
            else:
                # Verificar metadados se o caminho existir
                if self.caminho_pathlib.exists():
                    informacoes["metadados"] = self.obter_metadados()
                else:
                    info_combinadas["metadados"] = None
                    info_combinadas["erro"] = (
                        "O caminho não existe, não é possível obter metadados."
                    )

            # Obter caminhos resolvidos
            info_combinadas["caminho_relativo"] = self.converter_para_relativo()
            info_combinadas["caminho_absoluto"] = self.converter_para_absoluto()

            return info_combinadas
        except (OSError, ValueError, AttributeError) as e:
            print(f"Erro ao obter informações combinadas: {e}")
            return {}


# Exemplo de uso com os caminhos fornecidos
caminhos = [
    "../../Downloads/Chrome/",  # Exemplo de caminho relativo de pasta
    "../../Downloads/Chrome/favoritos_23_12_2024.html",  # Exemplo de caminho relativo de arquivo
]

# Instancia e realiza algumas operações com AnalisadorCaminhoIntegrado
diretorio_referencia = "/home/pedro-pm-dias/Downloads/Chrome"

for caminho in caminhos:
    analisador = AnalisadorCaminhoIntegrado(
        caminho_inicial=caminho, referencia_dir=diretorio_referencia
    )
    informacoes = analisador.obter_informacoes_combinadas()

    print(f"\nAnalisando o caminho: {caminho}")
    print("Informações combinadas:")
    for chave, valor in informacoes.items():
        print(f"{chave} => {valor}")
