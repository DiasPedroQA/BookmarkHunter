# app/models/file_model.py
# pylint: disable=C, R, E, W


import sys
import os
from pathlib import Path
from typing import Dict

# Caminho para a raiz do projeto (BookmarkHunter)
project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../.."
    )
)
if project_root not in sys.path:
    sys.path.append(project_root)

# Importações
from models.path_model import CaminhoBase


class Arquivo(CaminhoBase):
    """Classe para representar um arquivo."""

    def __init__(self, caminho: str):
        super().__init__(caminho)
        self.caminho_original = Path(caminho)
        self.eh_arquivo = self.caminho_original.is_file()
        self.eh_pasta = False

        # Validação adicional para garantir que é um arquivo
        if not self.eh_arquivo:
            raise ValueError(
                f"O caminho '{self.caminho_original}' não é um arquivo válido."
            )

    def caminho_absoluto(self) -> str:
        """Retorna o caminho absoluto do arquivo."""
        return str(self.caminho_original.absolute())

    def eh_link_simbolico(self) -> bool:
        """Verifica se o arquivo é um link simbólico."""
        return self.caminho_original.is_symlink()

    def eh_um_arquivo(self) -> bool:
        """Verifica se o caminho é um arquivo."""
        return self.caminho_original.is_file()

    def caminho_com_novo_nome(self, novo_nome: str) -> str:
        """Retorna um novo caminho com o mesmo diretório, mas com um novo nome."""
        return str(self.caminho_original.with_name(novo_nome))

    @property
    def nome_do_arquivo(self) -> str:
        """Retorna o nome do arquivo."""
        return self.caminho_original.name

    @property
    def nome_sem_extensao(self) -> str:
        """Retorna o nome do arquivo sem a extensão."""
        return self.caminho_original.stem

    def caminho_com_nova_extensao(self, nova_extensao: str) -> str:
        """Retorna um novo caminho com o mesmo nome, mas com uma nova extensão."""
        return str(self.caminho_original.with_suffix(nova_extensao))

    @property
    def extensao_do_arquivo(self) -> str:
        """Retorna a extensão do arquivo (incluindo o ponto)."""
        return self.caminho_original.suffix

    @property
    def todas_extensoes(self) -> list:
        """Retorna uma lista de todas as extensões do arquivo."""
        return self.caminho_original.suffixes

    def informacoes_do_arquivo(self):
        """Obtém informações sobre o arquivo."""
        try:
            return self.caminho_original.stat()
        except FileNotFoundError as error:
            print(error)
            raise ValueError(f"O arquivo '{self.caminho_original}' não foi encontrado.") from error

    def caminho_resolvido(self) -> str:
        """Resolve o caminho absoluto, considerando links simbólicos."""
        try:
            return str(self.caminho_original.resolve(strict=True))
        except FileNotFoundError as error:
            print(error)
            raise ValueError(f"O arquivo '{self.caminho_original}' não foi encontrado.") from error

    def ler_conteudo_como_texto(self, encoding: str = None) -> str:
        """Lê o conteúdo do arquivo como texto."""
        try:
            return self.caminho_original.read_text(encoding=encoding)
        except FileNotFoundError as error:
            print(error)
            raise ValueError(f"O arquivo '{self.caminho_original}' não foi encontrado.") from error
        except UnicodeDecodeError as error:
            print(error)
            raise ValueError("Erro ao decodificar o arquivo. Verifique o encoding.") from error

    def escrever_conteudo_como_texto(self, conteudo: str, encoding: str = None) -> None:
        """Escreve texto no arquivo."""
        try:
            self.caminho_original.write_text(conteudo, encoding=encoding)
        except Exception as error:
            raise ValueError(f"Erro ao escrever no arquivo: {error}") from error

    def dono_do_arquivo(self) -> str:
        """Retorna o proprietário do arquivo."""
        try:
            return self.caminho_original.owner()
        except PermissionError as error:
            print(error)
            raise ValueError(
                f"Permissão negada ao acessar o proprietário do arquivo '{self.caminho_original}'."
            ) from error

    def gerar_json(self):
        dados_arquivo = {
            "caminho_absoluto": self.caminho_absoluto(),
            "link_simbolico": self.eh_link_simbolico(),
            "eh_arquivo": self.eh_um_arquivo(),
            "nome_arquivo": self.nome_do_arquivo,
            "nome_sem_extensao": self.nome_sem_extensao,
            "extensao_arquivo": self.extensao_do_arquivo,
            "todas_extensoes": self.todas_extensoes,
            "informacoes_do_arquivo": self.informacoes_do_arquivo(),
            "caminho_resolvido": self.caminho_resolvido(),
            "dono_arquivo": self.dono_do_arquivo(),
        }
        dados_caminho = super().gerar_json()
        dados_caminho.update(dados_arquivo)
        return dados_caminho


tipos_de_caminhos: Dict[str, str] = {
    "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
    "Arquivo - Absoluto e inválido (caracteres proibidos)": "/home/pedro-pm-dias/arquivo?*<>.html",
    "Arquivo - Absoluto e inválido (link simbólico)": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_link_simbólico.html",
    "Arquivo - Absoluto e inválido (caminho inexistente)": "/home/pedro-pm-dias/Downloads/Chrome/arquivo_inexistente.html",
    "Arquivo - Relativo e válido (com data)": "../../Downloads/Chrome/favoritos_23_12_2024.html",
    "Arquivo - Relativo e válido (genérico)": "../../Downloads/Chrome/favoritos.html",
    "Arquivo - Relativo e inválido (caracteres proibidos)": "../imagens/arquivo?*<>.jpg",
    "Pasta - Absoluta e válida (Downloads)": "/home/pedro-pm-dias/Downloads/Chrome/",
    "Pasta - Absoluta e válida (Teste)": "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
    "Pasta - Absoluta e inválida (caminho inexistente)": "/caminho/inexistente/",
    "Pasta - Relativa e válida (Downloads)": "../../Downloads/Chrome/",
    "Pasta - Relativa e válida (Teste)": "../../Downloads/Chrome/Teste/",
}

for tipo, caminho in tipos_de_caminhos.items():
    print(f"\nTipo do caminho: {tipo}")
    caminho_obj = Arquivo(caminho=caminho)
    data = caminho_obj.gerar_json()
    print(data)
