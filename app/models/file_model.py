# pylint: disable=C, R, E, W

# Tabela 1: Dados de um Arquivo
# Método/Propriedade	Descrição
# .name	Nome do arquivo.
# .stem	Nome do arquivo sem a extensão.
# .suffix	Extensão do arquivo (incluindo o ponto).
# .suffixes	Lista de todas as extensões do arquivo, caso haja múltiplas.
# .is_file()	Verifica se o caminho é um arquivo.
# .stat()	Obtém informações sobre o arquivo, como tamanho, data de modificação e permissões.
# .absolute()	Retorna o caminho absoluto.
# .resolve()	Resolve o caminho absoluto, considerando links simbólicos.
# .with_name(new_name)	Retorna um novo caminho com o mesmo diretório, mas com um novo nome.
# .with_suffix(new_suffix)	Retorna um novo caminho com o mesmo nome, mas com uma nova extensão.
# .open(mode='r')	Abre o arquivo para leitura ou escrita.
# .read_bytes()	Lê todo o conteúdo do arquivo como bytes.
# .read_text(encoding=None)	Lê todo o conteúdo do arquivo como texto.
# .write_bytes(data)	Escreve bytes no arquivo.
# .write_text(data, encoding=None)	Escreve texto no arquivo.
# .is_symlink()	Verifica se o arquivo é um link simbólico.
# .owner()	Retorna o proprietário do arquivo (nome do usuário).
# .group()	Retorna o grupo ao qual o arquivo pertence.


# Exemplo de uso
# if __name__ == "__main__":
#     caminhos_para_validar: list[str] = [
#         "/caminho/inexistente/",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/",
#         "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#         "../../Downloads/Chrome/favoritos.html",
#         "../../Downloads/Chrome/favoritos_23_12_2024.html",
#         "../../Downloads/Chrome/",
#         "../../Downloads/Chrome/Teste/",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos_link_simbólico",  # Exemplo de link simbólico
#     ]
