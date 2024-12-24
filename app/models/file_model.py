# app/models/file_model.py
# pylint: disable=C, R0902

import os
import sys
from pathlib import Path
import platform
from typing import Optional, Dict

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.models.bookmark_model import ObjetoTag
from app.utils.conversores import ConversoresUtils
from app.utils.geradores import Geradores


class ObjetoArquivo:
    def __init__(self, caminho: str):
        self.caminho_atual = Path(caminho)
        self.conversores = ConversoresUtils()
        self.geradores = Geradores()
        self.caminho_absoluto = self.obter_caminho_absoluto()

    def _eh_caminho_absoluto(self) -> bool:
        """Verifica se o caminho é absoluto."""
        try:
            caminho_absoluto = self.caminho_atual.is_absolute()
            return caminho_absoluto
        except ValueError:
            return False

    def _obter_tamanho_arquivo(self) -> Optional[str]:
        """Obtém o tamanho de um arquivo em bytes."""
        try:
            return self.conversores.converter_tamanho_arquivo(tamanho_bytes=self.caminho_atual.stat().st_size)
        except FileNotFoundError:
            return None

    def obter_caminho_absoluto(self) -> Optional[Path]:
        """Obtém o caminho absoluto a partir do caminho atual."""
        if self._eh_caminho_absoluto():
            return self.caminho_atual
        try:
            return self.caminho_atual.resolve()
        except FileNotFoundError:
            return None

    def obter_informacoes_arquivo(self) -> Dict[str, Optional[str]]:
        """Obtém informações detalhadas sobre o arquivo."""
        informacoes_arquivo = {}
        if self.caminho_absoluto and self.caminho_absoluto.exists():
            # Informações sobre o caminho
            informacoes_arquivo['id_arquivo'] = self.geradores.gerar_id()
            informacoes_arquivo['sistema_operacional'] = platform.system()
            informacoes_arquivo['caminho_absoluto'] = str(self.caminho_absoluto)
            informacoes_arquivo['nome_arquivo'] = self.caminho_atual.name
            informacoes_arquivo['extensao_arquivo'] = self.caminho_atual.suffix
            informacoes_arquivo['diretorio_pai'] = self.obter_diretorio_pai()
            informacoes_arquivo['caminho_relativo'] = str(self.caminho_atual.relative_to(Path("/home/pedro-pm-dias")))
            informacoes_arquivo['is_file'] = self.caminho_atual.is_file()
            informacoes_arquivo['is_dir'] = self.caminho_atual.is_dir()
            informacoes_arquivo['tamanho_arquivo'] = self.conversores.converter_tamanho_arquivo(
                tamanho_bytes=self.caminho_atual.stat().st_size
            )
        return informacoes_arquivo

    def obter_diretorio_pai(self) -> Optional[Path]:
        """Obtém o diretório pai de um caminho."""
        return self.caminho_atual.parent

    def verificar_existencia_arquivo(self) -> bool:
        """Verifica se o arquivo existe."""
        try:
            caminho_existente = self.caminho_atual.exists()
            return caminho_existente
        except (FileExistsError, FileNotFoundError):
            print("O arquivo não existe.")
            return None

    def obter_datas_arquivo(self) -> Optional[str]:
        """Obtém a data de criação e de modificação de um arquivo."""
        try:
            data_criacao = self.caminho_atual.stat().st_ctime
            data_modificacao = self.caminho_atual.stat().st_mtime
            return self.conversores.converter_timestamp_arquivo(
                timestamp_criacao_arquivo=data_criacao,
                timestamp_modificacao_arquivo=data_modificacao
            )
        except FileNotFoundError:
            return None

    def ler_arquivo(self) -> Optional[str]:
        """Lê o conteúdo de um arquivo."""
        try:
            with open(self.caminho_atual, 'r', encoding="utf-8") as arquivo_lido:
                conteudo_tags = arquivo_lido.read()
                processos = ObjetoTag(conteudo_tags)
                return processos.processar_tags()
        except FileNotFoundError:
            return None

    def criar_novo_arquivo(self, conteudo_arquivo: str) -> bool:
        """Escreve conteúdo em um arquivo."""
        try:
            with open(self.caminho_atual, 'w', encoding="utf-8") as arquivo_novo:
                arquivo_novo.write(conteudo_arquivo)
            return True
        except FileNotFoundError:
            return False

    # def __criar_novo_caminho(self, nome_arquivo: str) -> Path:
    #     """Cria um novo caminho a partir do diretório e nome de arquivo."""
    #     return self.caminho_atual.parent / nome_arquivo

    # def __renomear_arquivo(self, sufixo: str, nova_extensao: str) -> Optional[Path]:
    #     """Renomeia um arquivo, incluindo um sufixo e nova extensão."""
    #     novo_nome = self.caminho_atual.stem + sufixo + nova_extensao
    #     novo_path = self.caminho_atual.parent / novo_nome
    #     self.caminho_atual.rename(novo_path)
    #     return novo_path

    # def __mover_arquivo(self, destino: str) -> Optional[Path]:
    #     """Move um arquivo para um novo caminho."""
    #     novo_path = Path(destino) / self.caminho_atual.name
    #     self.caminho_atual.replace(novo_path)
    #     return novo_path


# Exemplo de uso
caminho_exemplo = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
file_manager = ObjetoArquivo(caminho_exemplo)

# Obtendo informações do arquivo
informacoes = file_manager.obter_informacoes_arquivo()
print("Informações do arquivo:", informacoes)

# Obtendo a data de modificação do arquivo
datas = file_manager.obter_datas_arquivo()
print(f"Datas de criação e modificação: {datas}")

# # Lendo o conteúdo do arquivo
# conteudo = file_manager.__ler_arquivo()
# print(f"Conteúdo do arquivo: {conteudo}...")  # Exibindo as primeiras 100 linhas

# # Escrevendo no arquivo
# if file_manager.__criar_novo_arquivo("Novo conteúdo"):
#     print("Conteúdo escrito com sucesso.")

# # Renomeando o arquivo
# novo_nome_arquivo = file_manager.__renomear_arquivo("_processado", ".html")
# print(f"Arquivo renomeado para: {novo_nome_arquivo}")

# # Movendo o arquivo
# novo_caminho_move = file_manager.__mover_arquivo("/novo/caminho")
# print(f"Arquivo movido para: {novo_caminho_move}")
