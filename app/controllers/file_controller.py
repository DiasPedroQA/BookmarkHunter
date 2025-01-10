from app.services.file_service import FileService

class FileController:
    """Controlador para manipulação de arquivos e pastas."""

    def __init__(self):
        self.service = FileService()

    def analyze_path(self, path):
        """Orquestra a análise de arquivos no caminho."""
        return self.service.process_path(path)
