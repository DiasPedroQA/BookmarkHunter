import os
from app.repositories.file_repository import FileRepository
from models.file_analysis import FileAnalysis


class FileService:
    """Serviço que implementa as regras de negócio."""

    def __init__(self):
        self.repository = FileRepository()

    def process_path(self, path):
        """Processa um caminho, analisa arquivos e gera relatórios."""
        # Verificar se o caminho existe
        if not os.path.exists(path):
            raise ValueError("O caminho fornecido não existe.")

        # Identificar se é um arquivo ou uma pasta
        if os.path.isfile(path):
            files = [path]
        elif os.path.isdir(path):
            files = self.repository.list_txt_files(path)
        else:
            raise ValueError("Caminho inválido ou não suportado.")

        # Analisar cada arquivo e gerar resultados
        analyses = []
        for file in files:
            content = self.repository.read_file(file)
            analysis = FileAnalysis.analyze(content, file)
            self.repository.save_analysis(analysis, "output")
            analyses.append(analysis.to_dict())

        return {"analyses": analyses}
