# app/services/file_services.py
# """
# Este módulo contém funções auxiliares para manipulação de arquivos.

# Funções:
#     - obter_tamanho_arquivo(tamanho_arquivo: int) -> str:
#         Retorna o tamanho de um arquivo em formato legível (KB, MB, etc.).
# """

# def obter_tamanho_arquivo(tamanho_arquivo: int) -> str:
#     """
#     Converte o tamanho de um arquivo para um formato legível (KB, MB, etc.).

#     Args:
#         tamanho_arquivo (int): O tamanho do arquivo em bytes.

#     Returns:
#         str: O tamanho formatado com duas casas decimais e a unidade correspondente.

#     Raises:
#         ValueError: Se o tamanho for menor ou igual a zero.
#     """
#     if tamanho_arquivo <= 0:
#         raise ValueError("O tamanho deve ser maior que zero.")

#     unidades = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
#     contador = 0

#     while tamanho_arquivo >= 1024 and contador < len(unidades) - 1:
#         tamanho_arquivo /= 1024
#         contador += 1

#     return f"{tamanho_arquivo:.2f} {unidades[contador]}"
