from app.services.file_manager import FileManager
from app.services.text_analysis import TextAnalysis


class AnalysisController:
    """Controlador para análise de dados"""

    def __init__(self):
        self.file_manager = FileManager()
        self.text_analysis = TextAnalysis()

    def processar_dados(self, json_dados):
        """Processa os dados JSON do frontend"""
        # Simulação de carregamento e análise
        caminhos = self.file_manager.carregar_dados_json(json_dados)
        caminhos_filtrados = self.file_manager.filtrar_caminhos(caminhos)
        analise_resultados = self.text_analysis.analisar_caminhos(caminhos_filtrados)
        return analise_resultados
