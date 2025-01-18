# # pylint: disable=C, R, E, W

# """
# Testes para a função `obter_tamanho_arquivo` do módulo auxiliar de manipulação de arquivos.

# Funções testadas:
#     - obter_tamanho_arquivo: Verifica a formatação correta do tamanho do arquivo em unidades legíveis.
# """

# import pytest
# from app.services.file_services import obter_tamanho_arquivo


# @pytest.mark.parametrize(
#     "tamanho_arquivo, esperado",
#     [
#         (500, "500.00 Bytes"),  # Menor que 1 KB
#         (2048, "2.00 KB"),  # Igual a 2 KB
#         (1048576, "1.00 MB"),  # Igual a 1 MB
#         (1073741824, "1.00 GB"),  # Igual a 1 GB
#         (1099511627776, "1.00 TB"),  # Igual a 1 TB
#         (1125899906842624, "1.00 PB"),  # Igual a 1 PB
#         (1152921504606846976, "1.00 EB"),  # Igual a 1 EB
#     ],
# )
# def test_obter_tamanho_arquivo_sucesso(tamanho_arquivo: int, esperado: str) -> None:
#     """
#     Testa a função `obter_tamanho_arquivo` com valores válidos.

#     Args:
#         tamanho_arquivo (int): Tamanho do arquivo em bytes.
#         esperado (str): Resultado esperado após a conversão.
#     """
#     resultado = obter_tamanho_arquivo(tamanho_arquivo)
#     assert resultado == esperado


# @pytest.mark.parametrize(
#     "tamanho_arquivo",
#     [0, -1],  # Valores inválidos
# )
# def test_obter_tamanho_arquivo_valor_invalido(tamanho_arquivo: int) -> None:
#     """
#     Testa a função `obter_tamanho_arquivo` com valores inválidos.

#     Args:
#         tamanho_arquivo (int): Tamanho do arquivo em bytes.

#     Verifica:
#         - Levantamento da exceção `ValueError` quando o valor do tamanho for <= 0.
#     """
#     with pytest.raises(ValueError, match="O tamanho deve ser maior que zero."):
#         obter_tamanho_arquivo(tamanho_arquivo)
