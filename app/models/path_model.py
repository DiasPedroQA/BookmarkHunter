# app/models/analisador_string.py
# pylint: disable=C, R, E, W

import os
import sys
import json
from typing import Optional, Dict, Union
import uuid

# Adiciona o caminho raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Importações
from app.services.path_services import RegexPathAnalyzer


class CaminhoBase:
    def __init__(self, caminho_bruto: str):
        """
        Inicializa o objeto com os atributos principais.
        """
        self.caminho_original: str = caminho_bruto
        self._processar_caminho()

    @staticmethod
    def obter_id_unico(caminho: str) -> str:
        """
        Gera um UUID baseado em um caminho.
        """
        identificador = abs(hash(caminho))
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(identificador)))

    def _processar_caminho(self):
        """
        Processa o caminho e inicializa os atributos do objeto.
        """
        self.caminho_analisado = self.analises_caminho.analisar_caminho()
        

    def para_dict(self) -> Dict[str, Union[bool, int, None, str]]:
        """
        Converte os atributos do objeto para um dicionário.
        """
        return {
            "caminho_original": self.caminho_original,
            "id_unico": self.obter_id_unico(self.caminho_validado),
            "analises_caminho": RegexPathAnalyzer(self.caminho_original)
        }

    def gerar_json(self) -> str:
        """
        Gera uma representação JSON dos atributos do objeto.
        """
        return json.dumps(self.para_dict(), indent=4, ensure_ascii=False)


# Exemplo de uso
# if __name__ == "__main__":
#     tipos_de_caminhos: Dict[str, str] = {
#         "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "Arquivo - Relativo e válido": "../imagens/foto.jpg",
#         "Arquivo - Absoluto e inválido": "/home/pedro-pm-dias/arquivo?*<>.html",
#         "Arquivo - Relativo e inválido": "../imagens/arquivo?*<>.jpg",
#         "Pasta - Absoluta e válida": "/home/pedro-pm-dias/Downloads/Chrome/",
#         "Pasta - Relativa e válida": "./Downloads/Chrome/",
#         "Pasta - Absoluta e inválida": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
#         "Pasta - Relativa e inválida": "./Downloads/Chrome/<>/",
#     }

#     for tipo, caminho in tipos_de_caminhos.items():
#         print(f"\nTipo do caminho: {tipo}")
#         caminho_obj = CaminhoBase(caminho_bruto=caminho)
#         print(caminho_obj.gerar_json())

#     @staticmethod
#     def obter_estatisticas_caminho(caminho: str) -> Dict[str, int]:
#         """Obtém estatísticas sobre o caminho fornecido."""
#         estatisticas = Path(caminho).stat()
#         return {
#             "tamanho": estatisticas.st_size,
#             "data_acesso": RegexPathAnalyzer._obter_data_acesso(timestamp=estatisticas.st_atime),
#             "data_criacao": RegexPathAnalyzer._obter_data_criacao(timestamp=estatisticas.st_ctime),
#             "data_modificacao": RegexPathAnalyzer._obter_data_modificacao(timestamp=estatisticas.st_mtime),
#         }
