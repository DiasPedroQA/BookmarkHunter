def formatar_arquivo(arquivo):
    return {
        "id": arquivo.id,
        "nome": arquivo.nome,
        "tamanho": arquivo.tamanho,
        "descricao": f"{arquivo.nome} ({arquivo.tamanho})"
    }
