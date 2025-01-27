# pylint: disable=C, R, E, W
# tests/services/test___init__.py

# pylint: disable=C, R, E, W
# tests/services/test___init__.py

import sys
import os
import pytest
from app.services import RegexPathAnalyzer

# Adicionando o diretório raiz do projeto ao sys.path, se necessário
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Função de teste com o uso correto de pytest.raises
@pytest.mark.parametrize(
    "input_path, expected_exception",
    [
        (0, ValueError),  # Testa entrada inválida (não string)
        ("", ValueError),  # Testa entrada vazia
    ],
)
def test_regex_path_analyzer(input_path: str, expected_exception: type[ValueError] ) -> None:
    # Testa se a exceção correta é levantada para entradas inválidas
    with pytest.raises(expected_exception):
        analyzer = RegexPathAnalyzer(caminho_inicial=input_path)
        analyzer.analisar_caminho()
