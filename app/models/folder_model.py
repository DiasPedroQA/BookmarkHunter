# pylint: disable=C, R, E, W


# Tabela 2: Dados de uma Pasta (Diretório)
# Método/Propriedade	Descrição
# .name	Nome da pasta (diretório).
# .parent	Diretório pai da pasta.
# .parents	Lista de todos os diretórios pais da pasta.
# .is_dir()	Verifica se o caminho é um diretório.
# .exists()	Verifica se a pasta (diretório) existe.
# .absolute()	Retorna o caminho absoluto do diretório.
# .resolve()	Resolve o caminho absoluto do diretório, considerando links simbólicos.
# .relative_to(*other)	Retorna o caminho relativo ao diretório especificado.
# .joinpath(*other)	Concatena partes adicionais ao caminho da pasta.
# .glob(pattern)	Itera sobre arquivos/diretórios correspondentes a um padrão no diretório (não recursivo).
# .rglob(pattern)	Itera sobre arquivos/diretórios correspondentes a um padrão no diretório (recursivo).
# .iterdir()	Itera sobre os itens (arquivos e subdiretórios) no diretório.
# .mkdir(parents=True, exist_ok=True)	Cria um diretório (e diretórios pais, se especificado).
# .rmdir()	Remove o diretório.
# .is_symlink()	Verifica se o caminho é um link simbólico para um diretório.
# .owner()	Retorna o proprietário do diretório (nome do usuário).
# .group()	Retorna o grupo ao qual o diretório pertence.
