# app/models/analisador_string.py

"""
Classe para análise e manipulação de caminhos de arquivos e diretórios.
"""

import re
import json
import sys
import uuid
from pathlib import Path
from typing import Dict, Union

# Obtém o diretório raiz do projeto
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from services.global_services import GeneralServices


class CaminhoBase:
    """
    Representa um caminho de arquivo ou diretório, fornecendo métodos para
    análise, validação, sanitização e extração de informações.
    """

    def __init__(self, caminho_bruto: str):
        """
        Inicializa o objeto com o caminho fornecido.
        """
        self.caminho_original = caminho_bruto
        self.caminho_sanitizado = self._sanitizar_caminho(caminho=self.caminho_original)
        self.conversores = GeneralServices(caminho_inicial=self.caminho_sanitizado)

    @staticmethod
    def _sanitizar_caminho(caminho: str) -> str:
        """
        Sanitiza o caminho, removendo caracteres inválidos e normalizando barras.
        """
        caminho = caminho.strip()
        if not caminho or len(caminho) > 260:
            raise ValueError("Caminho inválido ou muito longo.")

        caminho = re.sub(r"[\\/]+", "/", caminho)
        return re.sub(r"[^a-zA-Z0-9:\- _./]", "", caminho)

    def validar_caminho(self) -> Dict[str, Union[bool, str]]:
        """
        Valida o caminho, verificando se é absoluto/relativo e se é arquivo/pasta.
        """
        try:
            # Converte o caminho sanitizado em um Path e resolve para absoluto
            path = Path(self.caminho_sanitizado).resolve()

            # Verifica se o caminho é absoluto ou relativo
            tipo = "absoluto" if path.is_absolute() else "relativo"

            # Verifica se é arquivo, pasta ou indefinido
            if path.exists():
                arquivo_ou_pasta = "arquivo" if path.is_file() else "pasta"
            else:
                arquivo_ou_pasta = "indefinido"

            return {
                "valido": True,
                "tipo": tipo,
                "arquivo_ou_pasta": arquivo_ou_pasta,
            }
        except (OSError, ValueError) as e:
            return {
                "valido": False,
                "tipo": f"inválido (erro: {str(e)})",
                "arquivo_ou_pasta": "indefinido",
            }

    def obter_metadados(self) -> Dict[str, Union[str, int, float]]:
        """
        Obtém metadados do arquivo ou diretório, como tamanho, datas de acesso, etc.
        """
        try:
            path = Path(self.caminho_sanitizado)
            if not path.exists():
                return {"erro": "O arquivo ou diretório não existe."}
            return {
                "[Tamanho em bytes]": self.conversores.obter_tamanho_bytes(),
                "[Tamanho formatado]": self.conversores.obter_tamanho_formatado(),
                "[Último acesso]": self.conversores.obter_ultimo_acesso(),
                "[Última modificação]": self.conversores.obter_ultima_modificacao(),
                "[Data de criação]": self.conversores.obter_data_criacao(),
                "[Permissões]": self.conversores.obter_permissoes(),
                "[Sistema operacional]": self.conversores.obter_sistema_operacional(),
            }
        except (OSError, ValueError) as e:
            return {"erro": f"Erro ao obter metadados: {str(e)}"}

    def gerar_json(self) -> str:
        """
        Gera uma representação JSON dos atributos do objeto.
        """
        dados = {
            "caminho_original": self.caminho_original,
            "id_unico": str(uuid.uuid5(uuid.NAMESPACE_DNS, self.caminho_sanitizado)),
            "caminho_sanitizado": self.caminho_sanitizado,
            "validacao": self.validar_caminho(),
            "metadados": self.obter_metadados(),
        }
        return json.dumps(dados, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Lista de caminhos para teste
    caminhos_teste = [
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "../../Downloads/Chrome/",
    ]

    for caminho_teste in caminhos_teste:
        print(f"\nAnalisando o caminho_teste: {caminho_teste}")
        analisador = CaminhoBase(caminho_teste)
        print(analisador.gerar_json())
        print("-" * 100)
